% =========================================================================
% Test code for Artifact-Reduction Convolutional Neural Networks (AR-CNN)
%
% Reference
%   Chao Dong, Yubin Deng, Chen Change Loy, Xiaoou Tang. Compression Artifacts Reduction by a Deep Convolutional Network, 
%   in Proceedings of International Conference on Computer Vision (ICCV), 2015
%
% Chao Dong
% IE Department, The Chinese University of Hong Kong
% For any question, send email to ndc.forward@gmail.com
% =========================================================================

clear,close all;

%% read ground truth image
dataset_name = 'live1';

image_files = dir (fullfile(dataset_name, '*.bmp'));

errs_j = [0; 0; 0; 0]
errs_d = [0; 0; 0; 0]
errs_a = [0; 0; 0; 0]

 for i = 1 : length(image_files)
    im_name = ['/' image_files(i).name]
    im  = imread([dataset_name im_name]);

    %% set parameters
    %JPEG_Quality = 10;
    %model = 'model\q10.mat';
    JPEG_Quality = 40;
    model_arcnn = ['model\q' int2str(JPEG_Quality) '.mat'];
    model = '../../models/e_default_colortarget';

    
    imwrite(im,'im_JPEG.jpg','jpg','Quality',JPEG_Quality);
    im_input = (im2double(imread('im_JPEG.jpg'))*255-16)/235;
    
    %% stack the color channels
    if size(im,3)>1
        im_ycbcr = rgb2ycbcr(im);
        im = im_ycbcr(:, :, :);
    end
    
    
    im_gnd = im;

    im_output = (imread([model '/' dataset_name im_name]));
    size_target = size(im_output);
    size_in = size(im_gnd);
    size_diff = size_in - size_target;
    crop_size = size_diff/2;
    
    im_input_y = rgb2ycbcr(im_input);
    
    im_arcnn = zeros(size(im_input_y));
    
    for ii = 1 :  3
        ar = ARCNN(model_arcnn, double(im_input_y(:,:,ii))-16/235);
        im_arcnn(:,:,ii) = ar;
    end
    
    
    im_gnd = imcrop(im_gnd, [crop_size(2)+1 crop_size(1)+1 size_target(2)-1 size_target(1)-1]);
    im_input_y = imcrop(im_input_y, [crop_size(2)+1 crop_size(1)+1 size_target(2)-1 size_target(1)-1]);
    im_arcnn = imcrop(im_arcnn, [crop_size(2)+1 crop_size(1)+1 size_target(2)-1 size_target(1)-1]);
    
    im_gnd = cat(1, im_gnd(:,:,1), im_gnd(:,:,2), im_gnd(:,:,3));
    im_arcnn = cat(1, im_arcnn(:,:,1), im_arcnn(:,:,2), im_arcnn(:,:,3));
    im_arcnn(im_arcnn>1) = 1;
    im_arcnn(im_arcnn<0) = 0;
    
    %% generate JPEG-compressed input
    
    im_input = cat(1, im_input_y(:,:,1), im_input_y(:,:,2), im_input_y(:,:,3));
    
    %im_arcnn = ARCNN(model_arcnn, im2double(im_input));
    im_output = (imread([model '/' dataset_name im_name]));
    im_output = cat(1, im_output(:,:,3), im_output(:,:,2), im_output(:,:,1));
    im_output = double(im_output)/235;%((double(im_output))/(235) - 16/235);
    
    im_output(im_output>1) = 1;
    im_output(im_output<0) = 0;
    
    im_gnd = (double(im_gnd-16)/235);
    
    
    %im_arcnn = (double(im_arcnn*255-16)/219);
    %im_arcnn(im_arcnn>1) = 1;
    %im_arcnn(im_arcnn<0) = 0;

    %% compute errors
    error_input = compute_errors(im_gnd, im_input);
    error_output = compute_errors(im_gnd, im_output);
    error_arcnn = compute_errors(im_gnd, ((im_arcnn*255)/235));
    
    errs_j = errs_j + error_input;
    errs_d = errs_d + error_output;
    errs_a = errs_a + error_arcnn;

    %% show results
    %figure, imshow(im_gnd); title('JPEG-compressed image');
    %figure, imshow(im_input); title('JPEG-compressed image');
    %figure, imshow(im_output); title('DDC-Net Reconstruction');
    %figure, imshow(im_arcnn); title('AR-CNN Reconstruction');

    %[e = imwrite(im_arcnn, ['live1/' '.bmp']);
    
    

 end
 
'PSNR, PSNR_B, BEF, SSIM for JPEG, DDC-NET and ARCNN'
errs_j / length(image_files)
errs_d / length(image_files)
errs_a / length(image_files)

