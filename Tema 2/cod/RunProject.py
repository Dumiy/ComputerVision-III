"""
    PROIECT
    REDIMENSIONEAZA IMAGINI.
    Implementarea a proiectului Redimensionare imagini
    dupa articolul "Seam Carving for Content-Aware Image Resizing", autori S. Avidan si A. Shamir
"""
import cv2 as cv
from Resize_Image import *
import matplotlib.pyplot as plt
def create(x,param1,param2,param3):
    image_name = '../data/'+x
    params = Parameters(image_name)

# seteaza optiunea de redimenionare
# micsoreazaLatime, micsoreazaInaltime, maresteLatime, maresteInaltime, amplificaContinut, eliminaObiect
    params.resize_option = param1
# numarul de pixeli pe latime
    params.num_pixels_width = param3[0]
# numarul de pixeli pe inaltime
    params.num_pixel_height = param3[1]
# afiseaza drumul eliminat
    params.show_path = True
# metoda pentru alegerea drumului
# aleator, greedy, programareDinamica
    params.method_select_path = param2
    resized_image = resize_image(params)
    resized_image_opencv = cv.resize(params.image, (resized_image.shape[1], resized_image.shape[0]))
    cv.imwrite(x+param1+param2+'.png',resized_image)
    cv.imwrite(x+param1+param2+'opencv'+'.png',resized_image_opencv)

func = ['micsoreazaLatime', 'micsoreazaInaltime', 'maresteLatime', 'maresteInaltime']
method = ['aleator', 'greedy', 'programareDinamica']
imagini = ['avion1.jpeg']
for x in imagini:
    for y in func:
        for z in method:
            create(x,y,z,[50,50])