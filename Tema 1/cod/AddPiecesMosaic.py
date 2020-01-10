from Parameters import *
import numpy as np
import pdb
import timeit
import cv2 as cv
from itertools import chain

def add_pieces_grid(params: Parameters):
    start_time = timeit.default_timer()
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape
    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal
    if params.criterion == 'aleator':
        for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
                index = np.random.randint(low=0, high=N, size=1)
                img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = params.small_images[index]
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))

    elif params.criterion == 'distantaCuloareMedie':
        if params.neighbours is False:
            mean_images = mean_small_images(params)
            for i in range(params.num_pieces_vertical):
                for j in range(params.num_pieces_horizontal):
                    index = find_most_similar(params.image_resized[i * H: (i + 1) * H, j * W: (j + 1) * W, :],mean_images)
                    img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = params.small_images[index]
                    print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))
        else:
            prev = -1
            mean_images = mean_small_images(params)
            map_neighbours = np.zeros(shape=(params.num_pieces_vertical,params.num_pieces_horizontal))
            for i in range(params.num_pieces_vertical):
                for j in range(params.num_pieces_horizontal):
                    index = find_most_similar(params.image_resized[i * H: (i + 1) * H, j * W: (j + 1) * W, :],
                                              mean_images)
                    if i == 0:
                        if j != 0:
                            if map_neighbours[i,j-1] == index:
                                temp = list(mean_images)
                                del temp[index]
                                #print(len(temp))
                                temporar = find_most_similar(params.small_images[index],
                                                          np.array(temp))
                                if temporar > index:
                                    index = temporar +1
                                else:
                                    index = temporar
                                map_neighbours[i][j] = index
                    elif i !=  0 and j == 0:
                        if map_neighbours[i-1,j] == index:
                            temp = list(mean_images)
                            del temp[index]
                            #print(len(temp))
                            temporar = find_most_similar(params.small_images[index],
                                                      np.array(temp))
                            if temporar > index:
                                index = temporar +1
                            else:
                                index = temporar
                            map_neighbours[i][j] = index
                    elif i != 0 and j != 0:
                        if map_neighbours[i-1,j] == index:
                            temp = list(mean_images)
                            del temp[index]
                            temporar = find_most_similar(params.small_images[index],
                                                      np.array(temp))
                            if temporar > index:
                                index = temporar+1
                            else:
                                index = temporar
                            map_neighbours[i,j] = index
                    if index == prev:
                        temp = list(mean_images)
                        del temp[index]
                        temporar = find_most_similar(params.small_images[index],
                                                np.array(temp))
                        if temporar > index:
                            index = temporar +1
                        else:
                            index = temporar
                        map_neighbours[i][j] = index
                    map_neighbours[i,j] = index
                    img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = params.small_images[index]
                    prev = index

                    print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))
            print(map_neighbours)
    else:
        print('Error! unknown option %s' % params.criterion)
        exit(-1)

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))
    return img_mosaic

def euclid_threedimension(a,b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)
def find_most_similar(original_piece,mean_images):
    index = 0
    mean_original_piece = np.mean(original_piece,axis=(0,1))
    temporary_matrix = mean_images[0]
    sum_of_piece = euclid_threedimension(mean_original_piece,temporary_matrix)
    for x in range(1,mean_images.shape[0]):
        sum_replace = euclid_threedimension(mean_original_piece,mean_images[x])
        if sum_replace < sum_of_piece:
            sum_of_piece = sum_replace
            index = x
    return index

def mean_small_images(params: Parameters):
    mean_images = []
    for x in params.small_images:
        mean_images.append(np.mean(x,axis=(0,1)))
    return np.array(mean_images)

def add_pieces_random(params: Parameters):
    start_time = timeit.default_timer()
    clarity = 4 # Variabila pentru a creste numarul de coordonate generate pentru random, astfel incat sa avem o claritate cat mai buna
    mean_images = mean_small_images(params)
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W, C = params.small_images.shape
    h,w,c = params.image_resized.shape
    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal
    first = np.random.randint(low=0, high=h-H, size=num_pieces*clarity)
    second = np.random.randint(low=0, high=w-W, size=num_pieces*clarity)
    first = first.flatten()
    second = second.flatten()
    if params.criterion == 'distantaCuloareMedie':
        for (x,y) in zip(first,second):
            index = find_most_similar(params.image_resized[x:x+H,y:y+W,:],mean_images)
            img_mosaic[x:x+H,y:y+W,:] = params.small_images[index]
    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))
    return img_mosaic

def add_pieces_hexagon(params: Parameters):
    return None
