"""
    PROIECT
    Sinteza si transferul texturii
    Implementarea a proiectului Sinteza si transferul texturii
    dupa articolul "Seam Carving for Content-Aware Image Resizing", autori Alexei A. Efros si William T. Freeman
"""

from Parameters import *
from CreateImage import *

from cod.Parameters import Parameters

image_name = '../data/img5.png'
params:Parameters = Parameters(image_name)

# dimensiunea imaginii ce urmeaza a fi construita
params.dim_result_image = (2 * params.image.shape[0], 2 * params.image.shape[1])
# numarul de blocuri ce vor fi extrase din imaginea originala
params.num_blocks = 2000
# dimensiunea blocurilor
params.dim_block = 36
# metoda de aranjare a blocurilor
# blocuriAleatoare, eroareSuprapunere, frontieraCostMinim, transfer
params.method = 'eroareSuprapunere'

metoda = ['blocuriAleatoare','eroareSuprapunere']
imagini = ['brick.jpg','img1.png','img9.png','radishes.jpg','img5.png']


for x in imagini:
    for y in metoda:
        params:Parameters = Parameters('../data/'+x)
        params.dim_result_image = (2 * params.image.shape[0], 2 * params.image.shape[1])
        params.num_blocks = 2000
        params.dim_block = 36
        params.method = y
        img = create_image(params)

        cv.imshow('img', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

        cv.imwrite(x+y+'.png',img)
