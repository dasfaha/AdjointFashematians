#!/usr/bin/python

import pyflann
import cPickle

from data_reader import read_training_data

import numpy as np

KNN_INDEX_PATH = 'models/knn_index.pk'
KNN_MATRIX_PATH = 'models/knn_matrix.pk'
KNN_PARAMS_PATH = 'models/knn_params.pk'

def train_matrix(train_matrix):
    flann = pyflann.FLANN()
    params = flann.build_index(train_matrix,
                               target_precision = 0.95,
                               log_level = 'info',
                               algorithm = 'autotuned')

    print('saving knn index to %s' % KNN_INDEX_PATH)
    flann.save_index(KNN_INDEX_PATH)

    print('saving knn matrix to %s' % KNN_MATRIX_PATH)
    f = open(KNN_MATRIX_PATH, 'w')
    cPickle.dump(train_matrix, f)
    f.close()

    print('saving knn params to %s' % KNN_PARAMS_PATH)
    f = open(KNN_PARAMS_PATH, 'w')
    cPickle.dump(params, f)
    f.close()

def run():
    nodes, edges, features = read_training_data()
    train_matrix(np.array([map(float, f) for f in features.values()]))

