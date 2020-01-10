import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pickle
import  pdb



from AddPiecesMosaic import *
from Parameters import *
def crop_hexagon(x):
    x = np.array(x)
    print(x.shape)
    middle_x = int(x.shape[0]/2)
    middle_y = int(x.shape[1]/2)
    upper_x = int(x.shape[1]/4)
    print(middle_y - upper_x,middle_y + upper_x)
    #x[0,:,:] = x[middle_x-upper_x:middle_x+upper_x]
    #x[x.shape[0]-1, :, :] = x[middle_x - upper_x:middle_x + upper_x]
    for i in range(0,middle_x):
        x[i, :, :] = x[i,middle_y - upper_x+i:middle_y + upper_x+i,:]
        x[x.shape[0] - i, :, :] = x[x.shape[0] - i,middle_y - upper_x+i:middle_y + upper_x+i,:]
    plt.imshow(x)
    plt.show()
def load_pieces(params: Parameters):

    if params.load_pickle is False:
        images = []
        files = os.listdir(params.small_images_dir)
        for file in files:
            img = cv.imread(os.path.join(params.small_images_dir, file))
            images.append(img)

        images = np.array(images)
        print(images.shape)
        #crop_hexagon(images[0])
        print(images.shape)
    if params.load_pickle is True:
        filenames = []
        images = []
        files = os.listdir(params.small_images_dir)
        for file in files:
            meta = unpickle(os.path.join(params.small_images_dir, file))
            data = meta[b'data']
            for d in data:
                image = np.zeros((32, 32, 3), dtype=np.uint8)
                image[..., 0] = np.reshape(d[:1024], (32, 32))  # Red channel
                image[..., 1] = np.reshape(d[1024:2048], (32, 32))  # Green channel
                image[..., 2] = np.reshape(d[2048:], (32, 32))  # Blue channel
                for (test,i) in zip(image,range(len(image))):
                    #cv.imwrite(str(i) + '.png', test[:,:,:])
                    pass
                images.append(image)
        images = np.array(images)
        images = images[6000*4:6000*5,:,:,:]
    if params.show_small_images:
        for i in range(10):
            for j in range(10):
                plt.subplot(10, 10, i * 10 + j + 1)
                # OpenCV reads images in BGR format, matplotlib reads images in RBG format
                im = images[i * 10 + j].copy()
                # BGR to RGB, swap the channels
                im = im[:, :, [2, 1, 0]]
                plt.imshow(im)
        plt.show()
    #images = np.transpose(images, (1, 2, 3, 0))
    params.small_images = images


def compute_dimensions(params: Parameters):
    # calculeaza dimensiunile mozaicului
    # obtine si imaginea de referinta redimensionata avand aceleasi dimensiuni
    # ca mozaicul
    if params.image.shape[0] < params.image.shape[1]:
        ratio = params.image.shape[0]/params.image.shape[1]
        params.num_pieces_vertical = int(params.num_pieces_horizontal * ratio)
    else:
        ratio = params.image.shape[1] / params.image.shape[0]
        params.num_pieces_vertical = params.num_pieces_horizontal + int(params.num_pieces_horizontal * ratio)
    # completati codul
    # calculeaza automat numarul de piese pe verticala
    print( params.num_pieces_vertical)
    # redimensioneaza imaginea
    new_h = (params.num_pieces_vertical*params.small_images.shape[1])
    new_w = (params.num_pieces_horizontal*params.small_images.shape[2])
    print(new_h,new_w)
    params.image_resized = cv.resize(params.image, (new_w, new_h))


def build_mosaic(params: Parameters):
    # incarcam imaginile din care vom forma mozaicul
    load_pieces(params)
    # calculeaza dimensiunea mozaicului
    compute_dimensions(params)

    img_mosaic = None
    if params.layout == 'caroiaj':
        if params.hexagon is True:
            img_mosaic = add_pieces_hexagon(params)
        else:
            img_mosaic = add_pieces_grid(params)
    elif params.layout == 'aleator':
        img_mosaic = add_pieces_random(params)
    else:
        print('Wrong option!')
        exit(-1)
    return img_mosaic
def unpickle(file):
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict

