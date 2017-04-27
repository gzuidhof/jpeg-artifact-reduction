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
im  = imread('LIVE1\womanhat.bmp');

%% set parameters
%JPEG_Quality = 10;
%model = 'model\q10.mat';
JPEG_Quality = 40;
model = 'model\q40.mat';

%% work on illuminance only
if size(im,3)>1
    im_ycbcr = rgb2ycbcr(im);
    im = im_ycbcr(:, :, 1);
end
im_gnd = im2double(im);

%% generate JPEG-compressed input
imwrite(im_gnd,'im_JPEG.jpg','jpg','Quality',JPEG_Quality);
im_input = im2double(imread('im_JPEG.jpg'));
       
%% conv1
im_output = ARCNN(model, im_input);

%% compute errors
error_input = compute_errors(im_gnd, im_input);
error_output = compute_errors(im_gnd, im_output);
    
%% show results
figure, imshow(im_input); title('JPEG-compressed image');
figure, imshow(im_output); title('AR-CNN Reconstruction');

imwrite(im_output, ['AR-CNN Reconstruction' '.bmp']);

