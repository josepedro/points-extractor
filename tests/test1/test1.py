#!/usr/bin/env python2

import unittest
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../../app')

from points_extractor import PointsExtractor
from PIL import Image

points = np.array([1, 2, 3, 4])
file_name = 'test1.png'
file_name_2 = 'test1_2.png'

def generate_plot():
    plt.plot(points)
    plt.ylabel('some numbers')
    plt.savefig('test1.png')
    plt.close()

class TestLinearPlot(unittest.TestCase):

    def setUp(self):
        generate_plot()

    def test_is_it_the_same(self):
        # im = Image.open(file_name_2)
        # im.save(file_name_2, dpi=(100,100))
        points_extractor = PointsExtractor(file_name_2)
        points_extractor.extract()

if __name__ == '__main__':
    unittest.main()
