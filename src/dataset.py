from __future__ import division
import numpy as np
import cv2

from functools import partial

from util import chunks

def _random_crop(image, crop_size=256):
    r_x = np.random.randint(image.shape[0]-crop_size)
    r_y = np.random.randint(image.shape[1]-crop_size)
    
    image = image[r_x:r_x+crop_size, r_y:r_y+crop_size]
    
    return image

def image_sample(filepath, quality_factor=20, crop_size=256, augment=True):
    image = cv2.imread(filepath, 0) #Read as grayscale

    if crop_size is not None:
        image = _random_crop(image, crop_size)

    if image.shape[0] > image.shape[1]:
        image = image.transpose(1,0)

    if augment:
        if np.random.randint(2) == 0:
            image = image[:,::-1]

        if np.random.randint(2) == 0:
            image = image[::-1, :]
        
    _, compresso = cv2.imencode('.jpg', image, (cv2.IMWRITE_JPEG_QUALITY, quality_factor))
    compressed_image = cv2.imdecode(compresso, 0)
    
    image = image.astype(np.float32) - 128
    compressed_image = compressed_image.astype(np.float32) - 128
    
    return np.expand_dims(image, axis=0), np.expand_dims(compressed_image, axis=0)

def images_sample(filepaths, quality_factor=20, crop_size=256, deterministic=False, residual=False):
    
    original, compressed = zip(* [image_sample(f, quality_factor, crop_size, (not deterministic)) for f in filepaths])

    original = np.array(original, dtype=np.float32)
    compressed = np.array(compressed, dtype=np.float32)

    goal = original
    if residual:
        goal = goal - compressed
    
    return compressed, goal
    
    


def get_image_generator(filenames, batch_size=32, quality_factor=20, crop_size=256, residual=False, deterministic=False):
    
    #samples_per_epoch = np.ceil(len(filenames)/batch_size)
    samples_per_epoch = len(filenames)
    filenames = list(filenames)

    sample_image_func = partial(image_sample, quality_factor=quality_factor, crop_size=crop_size, augment=(not deterministic))

    def genny():
        while True:
            
            np.random.shuffle(filenames)
        
            filename_batches = chunks(filenames, batch_size)
        
            for fb in filename_batches:
                original, compressed = zip(* map(sample_image_func, fb))
                original = np.array(original, dtype=np.float32)
                compressed = np.array(compressed, dtype=np.float32)

                goal = original
                if residual:
                    goal = goal - compressed
                
                yield compressed, goal
    
    return genny(), samples_per_epoch
