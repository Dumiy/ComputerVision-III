from Parameters import *
import numpy as np
import pdb

from cod import Parameters


def energy(E,Y):
        return np.sqrt(np.sum((E-Y)**2))
def compute_left(left_piece,right_piece,overlap):
    x = left_piece[:,-overlap:,:]
    y = right_piece[:,:overlap,:]
    z = energy(x,y)
    return z
def compute_up(left_piece,right_piece,overlap):
    x = left_piece[-overlap:,:,:]
    y = right_piece[:overlap,:,:]
    z = energy(x,y)
    return z


def add_overlapping(params: Parameters, blocks):
    overlap = int(params.dim_block / 6)

    n_blocks_x = int(np.ceil(params.dim_result_image[1] / params.dim_block))
    n_blocks_y = int(np.ceil(params.dim_result_image[0] / params.dim_block))

    if params.image.ndim == 3:
        aux_image = np.zeros(((n_blocks_y * params.dim_block)-overlap, (n_blocks_x * params.dim_block)-overlap, 3), np.uint8)
    else:
        aux_image = np.zeros(((n_blocks_y * params.dim_block)-overlap, (n_blocks_x * params.dim_block)-overlap, np.uint8))
    for y in range(n_blocks_y):
        for x in range(n_blocks_x):
            surplus = overlap
            if y == 0:
                if x == 0:
                    start_y = y * params.dim_block
                    end_y = start_y + params.dim_block
                    start_x = x * params.dim_block
                    end_x = start_x + params.dim_block
                    aux_image[start_y: end_y, start_x: end_x] = blocks[0]
                    temp = aux_image[start_y: end_y, start_x: end_x]
                else:
                    if x == n_blocks_x-1:
                        aux = aux_image.shape[1]-(x * params.dim_block-surplus)
                    blocuri = []
                    for z in blocks:
                        if np.allclose(z,temp):
                            pass
                        else:
                            blocuri.append(z)
                    blocuri = np.array(blocuri)
                    finding_piece = [compute_left(z[:,-overlap:,:], temp[:,-overlap:],overlap) for z in blocuri]
                    finding_piece = np.array(finding_piece)
                    start_y = y * params.dim_block
                    end_y = start_y + params.dim_block
                    start_x = x * params.dim_block -surplus
                    end_x = start_x + params.dim_block
                    piesa = blocks[np.where(finding_piece == min(finding_piece))[0][0]]
                    if x == n_blocks_x - 1:
                        aux_image[start_y: end_y, start_x: aux_image.shape[1]] = piesa[:,-aux:,:]
                        last_piece =  piesa[:,-aux:,:]
                    else:
                        aux_image[start_y: end_y, start_x: end_x] = piesa
                        temp = aux_image[start_y: end_y, start_x: end_x]
            else:
                if x == 0:
                    aux_up =  aux_image[(y-1) * params.dim_block:((y-1) * params.dim_block )+ params.dim_block, x * params.dim_block: params.dim_block]
                    blocuri = []
                    for z in blocks:
                        if np.allclose(z, aux_up):
                            pass
                        else:
                            blocuri.append(z)
                    blocuri = np.array(blocuri)
                    finding_piece = [compute_up(z[-overlap:,:,:],aux_up[-overlap:,:,:],overlap) for z in blocuri]
                    finding_piece = np.array(finding_piece)
                    start_y = y * (params.dim_block -surplus)
                    end_y = start_y + params.dim_block
                    start_x = x * params.dim_block
                    end_x = start_x + params.dim_block
                    aux_image[start_y: end_y, start_x: end_x] = blocks[np.where(finding_piece == np.min(finding_piece))[0][0]]
                    temp = aux_image[y: params.dim_block, x: params.dim_block]
                else:
                    if x == n_blocks_x-1:
                        aux = aux_image.shape[1]-(x * params.dim_block-surplus)
                        aux_up = last_piece
                    if x == 0:
                        if y == 1:
                            aux_up = aux_image[(y - 1) * params.dim_block:(y - 1) * params.dim_block + params.dim_block,(x) * params.dim_block: (x) * params.dim_block + params.dim_block]
                        else:
                            aux_up = aux_image[(y - 1) * params.dim_block-y*surplus:(y - 1) * params.dim_block + params.dim_block-y*surplus,(x) * params.dim_block: (x) * params.dim_block + params.dim_block]
                    if x !=0 and x!=n_blocks_x-1:
                        if y == 1:
                            aux_up = aux_image[(y - 1) * params.dim_block:(y - 1) * params.dim_block + params.dim_block,x * params.dim_block-surplus: x  * params.dim_block + params.dim_block-surplus]
                        else:
                            aux_up = aux_image[(y - 1) * params.dim_block-(y*surplus):(y - 1) * params.dim_block + params.dim_block-y*surplus,x * params.dim_block-surplus: x  * params.dim_block + params.dim_block-surplus]
                    blocuri = []
                    for z in blocks:
                        if np.allclose(z, aux_up):
                            pass
                        else:
                            blocuri.append(z)
                    blocuri = np.array(blocuri)
                    finding_piece = [compute_up(z[-overlap:,:,:],aux_up[-overlap:,:,:],overlap) for z in blocuri]
                    finding_piece = np.array(finding_piece)
                    start_y = y * (params.dim_block -surplus)
                    end_y = start_y + params.dim_block
                    start_x = x * params.dim_block
                    end_x = start_x + params.dim_block
                    piese = blocks[np.where(finding_piece == np.min(finding_piece))[0][0]]
                    blocuriv2 = []
                    for z in blocuri:
                        if np.allclose(z, aux_up):
                            pass
                        else:
                            blocuriv2.append(z)
                    blocuriv2= np.array(blocuriv2)
                    finding_piece = [compute_left(z[:,-overlap:,:], piese[:,-overlap:,:], overlap) for z in blocuriv2]
                    finding_piece = np.array(finding_piece)
                    piese = blocks[np.where(finding_piece == np.min(finding_piece))[0][0]]
                    if x == n_blocks_x - 1:
                        aux_image[start_y: end_y, start_x-surplus: aux_image.shape[1]] = piesa[:,-aux:,:]
                    else:
                        aux_image[start_y: end_y, start_x: end_x] = piese
                        temp = aux_image[y: params.dim_block, x: params.dim_block]
    return aux_image[:end_y, :end_x, :]
def add_random_blocks(params: Parameters, blocks):
    n_blocks_x = int(np.ceil(params.dim_result_image[1] / params.dim_block))
    n_blocks_y = int(np.ceil(params.dim_result_image[0] / params.dim_block))
    if params.image.ndim == 3:
        aux_image = np.zeros((n_blocks_y * params.dim_block, n_blocks_x * params.dim_block, 3), np.uint8)
    else:
        aux_image = np.zeros((n_blocks_y * params.dim_block, n_blocks_x * params.dim_block), np.uint8)

    for y in range(n_blocks_y):
        for x in range(n_blocks_x):
            idx = np.random.randint(low=0, high=len(blocks), size=1)[0]
            start_y = y * params.dim_block
            end_y = start_y + params.dim_block
            start_x = x * params.dim_block
            end_x = start_x + params.dim_block
            aux_image[start_y: end_y, start_x: end_x] = blocks[idx]

    result_image = aux_image[:params.dim_result_image[0], :params.dim_result_image[1]]
    return result_image


def create_image(params: Parameters):

    img_h = params.image.shape[0]
    img_w = params.image.shape[1]
    # generate random positions
    result_image = None
    y = np.random.randint(low=0, high=img_h - params.dim_block, size=params.num_blocks)
    x = np.random.randint(low=0, high=img_w - params.dim_block, size=params.num_blocks)
    blocks = []
    for idx in range(params.num_blocks):
        pos_y = y[idx]
        pos_x = x[idx]
        blocks.append(params.image[pos_y: pos_y + params.dim_block, pos_x: pos_x + params.dim_block])
    blocks = np.array(blocks, np.float32)
    if params.method == "blocuriAleatoare":
        result_image = add_random_blocks(params, blocks)
    if params.method == "eroareSuprapunere":
        result_image = add_overlapping(params,blocks)

    return result_image
