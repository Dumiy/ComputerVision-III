import numpy as np
import cv2 as cv
import os
import pdb
import gc


class DataSet:

    def __init__(self):
        self.scene_name = 'coast'  # numele scenei:  forest/coast
        self.training_dir = '../data/%s/training' % self.scene_name
        self.test_dir = '../data/%s/test' % self.scene_name
        self.dir_output_images = '../data/output_images/%s' % self.scene_name
        if not os.path.exists(self.dir_output_images):
            os.makedirs(self.dir_output_images)

        self.network_input_size = (64, 64)  # dimensiunea imaginilor de antrenare
        self.input_training_images,  self.ground_truth_training_images, self.ground_truth_bgr_training_images =\
            self.read_images(self.training_dir)
        self.input_test_images, self.ground_truth_test_images, self.ground_truth_bgr_test_images =\
            self.read_images(self.test_dir)

    def read_images(self, base_dir):
        files = os.listdir(base_dir)
        in_images = []  # imaginile de input, canalul L din reprezentarea Lab.
        gt_images = []  # imaginile de output (ground-truth), canalele ab din reprezentarea Lab.
        bgr_images = []  # imaginile in format BGR.
        for file in files:
            # citim imaginea
            bgr_image = cv.imread(os.path.join(base_dir+"/"+file))
            # redimensionam imaginea conform parametrului self.network_input_size.
            if bgr_image is not None:
                bgr_image = cv.resize(bgr_image,self.network_input_size)
            # convertim imaginea in reprezentarea Lab.
                lab_image = cv.cvtColor(np.ﬂoat32(bgr_image) / 255, cv.COLOR_BGR2LAB)
            # luam canalul L.
                gray_image = lab_image[:,:,0]
                gray_image = np.array(gray_image[...,np.newaxis])
            # luam canalale ab si le impartim la 128.
                ab_image = lab_image[:,:,1:]/128
                in_images.append(gray_image)
                gt_images.append(ab_image)
                bgr_images.append(bgr_image)
        return np.array(in_images, np.float32), np.array(gt_images, np.float32), np.array(bgr_images, np.float32)
