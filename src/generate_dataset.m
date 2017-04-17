%splits = {'train','val','test'};
splits = {''};
quality_factor = 20;

for j = 1: length(splits)
    split = splits{j}
    %in_folder = ['../data/BSDS500/data/images/' split];
    %out_folder = ['../data/BSDS500/data/images_compressed_' num2str(quality_factor) '/' split];
    in_folder = ['E:/RAISE_4k_downsampled/'];
    out_folder = ['E:/RAISE_4k_downsampled_compressed_' num2str(quality_factor)];
    
    % May fail, but then the folder already exists (hopefully), so no biggie
    s = mkdir(out_folder);

    %image_files = dir (fullfile(in_folder, '*.jpg'));
    image_files = dir (fullfile(in_folder, '*.tif'));

    for i = 1 : length(image_files)
        image = imread(fullfile(in_folder,image_files(i).name));
        imwrite(image,fullfile(out_folder,image_files(i).name),'jpg','Quality',quality_factor);
    end
end
