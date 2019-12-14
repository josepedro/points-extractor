#!/usr/bin/env python2

import unittest
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../../app')

from points_extractor import PointsExtractor

points = np.array([1, 2, 3, 4])
file_name = 'test1.png'

def generate_plot():
    plt.plot(points)
    plt.ylabel('some numbers')
    plt.savefig('test1.png')

class TestLinearPlot(unittest.TestCase):

    def setUp(self):
        generate_plot()

    def test_is_it_the_same(self):
        points_extractor = PointsExtractor(file_name)
        points_extractor.extract()

if __name__ == '__main__':
    unittest.main()
