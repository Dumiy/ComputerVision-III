import sys
import cv2 as cv
import numpy as np
from scipy import ndimage
from skimage import filters
import matplotlib.pyplot as plt


from Parameters import *
from SelectPath import *

import pdb


def compute_energy(img):
    img_gray_scale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    dx = ndimage.sobel(img_gray_scale.astype(np.float32),0)
    dy = ndimage.sobel(img_gray_scale.astype(np.float32),1)
    E = np.sqrt((dx)**2+(dy)**2)
    #E = filters.sobel(img_gray_scale.astype(np.float32))
    return E


def show_path(img, path, color):
    new_image = img.copy()
    for row, col in path:
        new_image[row, col] = color

    cv.imshow('path', np.uint8(new_image))
    cv.waitKey(100)


def delete_path_vertical(img, pathway):
    updated_img = np.zeros((img.shape[0], img.shape[1] - 1, img.shape[2]), np.uint8)
    for i in range(img.shape[0]):
        col = pathway[i][1]
        updated_img[i, :col] = img[i, :col].copy()
        if col == 0:
            updated_img[i, col:] = img[i, col+1:].copy()
        if col != 0:
            updated_img[i,col-1:] = img[i,col:].copy()
    return updated_img


def delete_path_orizontal(img, pathway):
    updated_img = np.zeros((img.shape[0] -1 , img.shape[1], img.shape[2]), np.uint8)
    for i in range(img.shape[1]):
        lin = pathway[i][0]
        updated_img[:lin, i] = img[:lin,i].copy()
        if lin == 0:
            updated_img[lin:, i] = img[lin+1:, i].copy()
        if lin != 0:
            updated_img[lin-1:,i] = img[lin:,i].copy()
    return updated_img


def increase_path_orizontal(img, pathway):
    print(pathway)
    updated_img = np.zeros((img.shape[0] +1 , img.shape[1], img.shape[2]), np.uint8)
    for i in range(img.shape[1]):
        lin = pathway[i][0]
        updated_img[:lin, i] = img[:lin,i].copy()
        if lin == 0:
            updated_img[lin+1:, i] = img[lin:, i].copy()
        if lin != 0:
            updated_img[lin+1:,i] = img[lin:,i].copy()
        updated_img[lin, i] = img[lin,i].copy()
    return updated_img



def increase_path_vertical(img, pathway):
    updated_img = np.zeros((img.shape[0], img.shape[1] + 1, img.shape[2]), np.uint8)
    for i in range(img.shape[0]):
        col = pathway[i][1]
        updated_img[i, :col] = img[i, :col].copy()
        if col == 0:
            updated_img[i, col+1:] = img[i, col:].copy()
        if col != 0:
            updated_img[i, col+1:] = img[i,col:].copy()
        updated_img[i,col] = img[i,col].copy()
    return updated_img



def decrease_width(params: Parameters, num_pixels):
    img = params.image.copy() # copiaza imaginea originala
    for i in range(num_pixels):
        print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i + 1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img)
        path = select_path(E, params.method_select_path,'width')
        if path is None:
            break
        if params.show_path:
            show_path(img, path, params.color_path)
        img = delete_path_vertical(img, path)

    cv.destroyAllWindows()
    return img

def decrease_height(params: Parameters, num_pixels):
    img = params.image.copy() # copiaza imaginea originala
    for i in range(num_pixels):
        print('Eliminam drumul orizontala numarul %i dintr-un total de %d.' % (i + 1, num_pixels))
        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img)
        path = select_path(E, params.method_select_path,'height')
        if params.show_path:
            show_path(img, path, params.color_path)
        img = delete_path_orizontal(img, path)
    cv.destroyAllWindows()
    return img

def increase_height(params: Parameters, num_pixels):
    img = params.image.copy() # copiaza imaginea originala
    for i in range(num_pixels):
        print('Adaugam drumul orizontala numarul %i dintr-un total de %d.' % (i + 1, num_pixels))
        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img)
        path = select_path(E, params.method_select_path,'height')
        if params.show_path:
            show_path(img, path, params.color_path)
        img = increase_path_orizontal(img, path)
    cv.destroyAllWindows()
    return img


def increase_width(params: Parameters, num_pixels):
    img = params.image.copy() # copiaza imaginea originala
    for i in range(num_pixels):
        print('Adaugam drumul verticala numarul %i dintr-un total de %d.' % (i + 1, num_pixels))
        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img)
        path = select_path(E, params.method_select_path,'width')
        if path is None:
            break
        if params.show_path:
            show_path(img, path, params.color_path)
        img = increase_path_vertical(img, path)
    cv.destroyAllWindows()
    return img



def resize_image(params: Parameters):

    if params.resize_option == 'micsoreazaLatime':
        # redimensioneaza imaginea pe latime
        resized_image = decrease_width(params, params.num_pixels_width)
        return resized_image
    elif params.resize_option == 'micsoreazaInaltime':
        resized_image = decrease_height(params,params.num_pixel_height)
        return resized_image
    elif params.resize_option == 'maresteLatime':
        resized_image = increase_width(params, params.num_pixels_width)
        return resized_image
    elif params.resize_option == 'maresteInaltime':
        resized_image = increase_height(params,params.num_pixel_height)
        return resized_image
    elif params.resize_option == 'amplificaContinut':
        pass
    elif params.resize_option == 'eliminaObiect':
        # elimina obiect din imagine
        pass
    else:
        print('The option is not valid!')
        sys.exit(-1)
