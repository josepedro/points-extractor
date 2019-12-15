#!/usr/bin/env python2

import numpy as np
import matplotlib.pyplot as plt
import xml.dom.minidom
import matplotlib.image as mpimg
from scipy.misc import imread, imsave

import sys
sys.setrecursionlimit(100000)

class Element(object):
    def __init__(self):
        # [x,y]
        self.points = []
    def insert_point(self, point): # np.array([x,y])
        has_point = False
        for point_element in self.points:
            if point_element[0] == point[0] and point_element[1] == point[1]:
                has_point = True
        if has_point == False:
            self.points.append(point)
        return has_point

    def compute_geometric_center(self,image):
        min_distance = 9999
        image_geometric_center_x = image.shape[1]/2.0
        image_geometric_center_y = image.shape[0]/2.0
        magnitude_image = np.sqrt(image_geometric_center_x**2 + image_geometric_center_y**2)
        for point in self.points:
            magnitude_point = np.sqrt(point[1]**2 + point[0]**2)
            distance_from_center = np.abs(magnitude_point - magnitude_image)
            if distance_from_center < min_distance:
                min_distance = distance_from_center
        self.distance_from_center = min_distance
        

class PointsExtractor(object):
    
    """docstring for PointsExtractor"""
    
    def __init__(self, file_name):
        self.file_name = file_name

    def __fill_recursively(self, image, element, y, x):
        has_point = element.insert_point(np.array([y,x]))
        if has_point:
            return element
        ''' 1 2 3
            4 5 6
            7 8 9
            indeed we are on the slot 5
        '''
        # check neighbor 1
        point_neighbor_x = x - 1
        point_neighbor_y = y + 1
        if (point_neighbor_x < image.shape[1] and point_neighbor_y < image.shape[0] and
            image[point_neighbor_y][point_neighbor_x] == 0 and 
            point_neighbor_x >= 0 and point_neighbor_y >= 0):
            element = self.__fill_recursively(image, element, 
                        point_neighbor_y, point_neighbor_x)

        # check neighbor 2
        point_neighbor_x = x
        point_neighbor_y = y + 1
        if (point_neighbor_x < image.shape[1] and point_neighbor_y < image.shape[0] and
            image[point_neighbor_y][point_neighbor_x] == 0 and 
            point_neighbor_x >= 0 and point_neighbor_y >= 0):
            element = self.__fill_recursively(image, element, 
                        point_neighbor_y, point_neighbor_x)

        # check neighbor 3
        point_neighbor_x = x + 1
        point_neighbor_y = y + 1
        if (point_neighbor_x < image.shape[1] and point_neighbor_y < image.shape[0] and
            image[point_neighbor_y][point_neighbor_x] == 0 and 
            point_neighbor_x >= 0 and point_neighbor_y >= 0):
            element = self.__fill_recursively(image, element, 
                        point_neighbor_y, point_neighbor_x)

        # check neighbor 4
        point_neighbor_x = x - 1
        point_neighbor_y = y 
        if (point_neighbor_x < image.shape[1] and point_neighbor_y < image.shape[0] and
            image[point_neighbor_y][point_neighbor_x] == 0 and 
            point_neighbor_x >= 0 and point_neighbor_y >= 0):
            element = self.__fill_recursively(image, element, 
                        point_neighbor_y, point_neighbor_x)

        # check neighbor 6
        point_neighbor_x = x + 1
        point_neighbor_y = y 
        if (point_neighbor_x < image.shape[1] and point_neighbor_y < image.shape[0] and
            image[point_neighbor_y][point_neighbor_x] == 0 and 
            point_neighbor_x >= 0 and point_neighbor_y >= 0):
            element = self.__fill_recursively(image, element, 
                        point_neighbor_y, point_neighbor_x)

        # check neighbor 7
        point_neighbor_x = x - 1
        point_neighbor_y = y - 1
        if (point_neighbor_x < image.shape[1] and point_neighbor_y < image.shape[0] and
            image[point_neighbor_y][point_neighbor_x] == 0 and 
            point_neighbor_x >= 0 and point_neighbor_y >= 0):
            element = self.__fill_recursively(image, element, 
                        point_neighbor_y, point_neighbor_x)

        # check neighbor 8
        point_neighbor_x = x
        point_neighbor_y = y - 1
        if (point_neighbor_x < image.shape[1] and point_neighbor_y < image.shape[0] and
            image[point_neighbor_y][point_neighbor_x] == 0 and 
            point_neighbor_x >= 0 and point_neighbor_y >= 0):
            element = self.__fill_recursively(image, element, 
                        point_neighbor_y, point_neighbor_x) 

        # check neighbor 9
        point_neighbor_x = x + 1
        point_neighbor_y = y - 1
        if (point_neighbor_x < image.shape[1] and point_neighbor_y < image.shape[0] and
            image[point_neighbor_y][point_neighbor_x] == 0 and 
            point_neighbor_x >= 0 and point_neighbor_y >= 0):
            element = self.__fill_recursively(image, element, 
                        point_neighbor_y, point_neighbor_x)


        return element

    
    def __build_element(self, image, y, x):
        element = Element()
        element = self.__fill_recursively(image, element, y, x)
        element.compute_geometric_center(image)
        return element


    def __delete_element_on_binarized(self, image, element):
        for point in element.points:
            image[point[0]][point[1]] = 1
        return image


    def __process(self, binarized):
        
        # above
        max_column = binarized.shape[0]
        max_row = binarized.shape[1]
        is_it_cut = False
        for column in range(max_column):
            for row in range(max_row):
                if binarized[column][row] == 0.0:
                    binarized = binarized[column:max_column-1][0:max_row-1]
                    is_it_cut = True
                    break
            if is_it_cut:
                break

        # below
        max_column = binarized.shape[0]
        max_row = binarized.shape[1]
        is_it_cut = False
        for column in np.flip(np.arange(max_column)):
            for row in np.flip(np.arange(max_row)):
                if binarized[column][row] == 0.0:
                    binarized = binarized[0:column+1][0:max_row-1]
                    is_it_cut = True
                    break
            if is_it_cut:
                break                
        
        # left
        max_column = binarized.shape[0]
        max_row = binarized.shape[1]
        is_it_cut = False
        for row in range(max_row):
            for column in range(max_column):
                if binarized[column][row] == 0.0:
                    binarized =  np.delete(binarized,np.arange(row),1)
                    is_it_cut = True
                    break
            if is_it_cut:
                break

        # right
        max_column = binarized.shape[0]
        max_row = binarized.shape[1]
        is_it_cut = False
        for row in np.flip(np.arange(max_row)):
            for column in np.flip(np.arange(max_column)):
                if binarized[column][row] == 0.0:
                    binarized =  np.delete(binarized,np.arange(row, max_row-1),1)
                    is_it_cut = True
                    break
            if is_it_cut:
                break

        # -------------------------------------------------------------
        # Elements
        max_column = binarized.shape[0]
        max_row = binarized.shape[1]
        list_elements_found = []
        while (np.any(binarized == 0.0)):
            found_0 = False
            for y in np.arange(max_column):
                for x in np.arange(max_row):
                    if binarized[y][x] == 0:
                        found_0 = True
                        element_found = self.__build_element(binarized, y, x)
                        list_elements_found.append(element_found)
                        binarized = self.__delete_element_on_binarized(binarized,element_found)
                        break
                if found_0:
                    break

        element_id = 0
        it = 0
        min_geometric_distance = 9999
        distances = []
        for element in list_elements_found:
            distances.append(element.distance_from_center)
            if element.distance_from_center < min_geometric_distance:
                min_geometric_distance = element.distance_from_center
                element_id = it
            it += 1

        for point in list_elements_found[element_id].points:
            plt.scatter(point[1], point[0])
        plt.show()
        import pdb; pdb.set_trace()
        imgplot = plt.imshow(binarized, 'gray')
        plt.show()


    def extract(self):
        print('extrating')
        img = np.flipud(imread(self.file_name, mode='L'))
        binarized = 1.0 * (img > np.mean(img))
        self.__process(binarized)



        import pdb; pdb.set_trace()
        imgplot = plt.imshow(binarized, 'gray')
        plt.show()    



    
