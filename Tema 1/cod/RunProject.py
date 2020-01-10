"""
    PROIECT MOZAIC
"""

# Parametrii algoritmului sunt definiti in clasa Parameters.
from Parameters import *
from BuildMosaic import *



# numele imaginii care va fi transformata in mozaic
image_path = './../data/imaginiTest/caz.jpg'
params = Parameters(image_path)

# directorul cu imagini folosite pentru realizarea mozaicului
params.small_images_dir = './../data/colectie/'
# tipul imaginilor din director
params.image_type = 'png'
# numarul de piese ale mozaicului pe orizontala
# pe verticala vor fi calcultate dinamic a.i sa se pastreze raportul
#params.num_pieces_horizontal =  100
# afiseaza piesele de mozaic dupa citirea lor
params.show_small_images = False
# modul de aranjarea a pieselor mozaicului
# optiuni: 'aleator', 'caroiaj'
params.layout = 'caroiaj'
#parametru pentru vecini diferiti sus jos stanga dreapta
params.neighbours = True
# criteriul dupa care se realizeaza mozaicul
# optiuni: 'aleator', 'distantaCuloareMedie'
params.criterion = 'distantaCuloareMedie'
# daca params.layout == 'caroiaj', sa se foloseasca piese hexagonale
#params.hexagon = False
params.load_pickle = False
for x in [200]:
    params.num_pieces_horizontal = x
    img_mosaic = build_mosaic(params)
    cv.imwrite(str(x) + 'mozaic.png' , img_mosaic)


