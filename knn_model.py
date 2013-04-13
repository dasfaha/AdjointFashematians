#!/usr/bin/python

import pyflann
import cPickle
import math

from data_reader import read_training_data

import numpy as np

KNN_INDEX_PATH = 'models/knn_index.pk'
KNN_MATRIX_PATH = 'models/knn_matrix.pk'
KNN_PARAMS_PATH = 'models/knn_params.pk'
KNN_SCALER_PARAMS_PATH = 'models/knn_scaler_params.pk'

def scale_features(x):
    params = []
    for i, column in enumerate(x.transpose()):
        mean = sum(column)/len(column)
        variance = sum(map(lambda x: (x-mean)**2, column))/len(column)
        sd = math.sqrt(variance)
        params.append([mean,sd])
        if sd != 0:
            scaled_column = (column-mean)/sd
        else:
            scaled_column = column-mean
        x[:,i] = scaled_column
    return params

def fit_scale_features(features, scaler_params):
    for i,f in enumerate(features):
        mean, sd = scaler_params[i]
        if sd == 0:
            scaled_feature = f-mean
        else:
            scaled_feature = (f-mean)/sd
        features[i] = scaled_feature
    return features

def train_matrix(train_matrix):
    scaler_params = scale_features(train_matrix)

    print('saving knn scaler params to %s' % KNN_SCALER_PARAMS_PATH)
    f = open(KNN_SCALER_PARAMS_PATH, 'w')
    cPickle.dump(scaler_params, f)
    f.close()

    flann = pyflann.FLANN()
    params = flann.build_index(train_matrix,
                               target_precision = 0.95,
                               log_level = 'info',
                               algorithm = 'composite',
                               branching = 32,
                               iterations = 16)

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

def predict(feature_vector):
        print("loading knn matrix from %s" % KNN_MATRIX_PATH)
        f = open(KNN_MATRIX_PATH, 'r')
        knn_matrix = cPickle.load(f)
        f.close()

        print("loading knn model params from %s" % KNN_PARAMS_PATH)
        f = open(KNN_PARAMS_PATH, 'r')
        knn_params = cPickle.load(f)
        f.close()

        print("loading knn scaler params from %s" % KNN_SCALER_PARAMS_PATH)
        f = open(KNN_SCALER_PARAMS_PATH, 'r')
        scaler_params = cPickle.load(f)
        f.close()

        print("loading knn index from %s" % KNN_INDEX_PATH)
        knn_model = pyflann.FLANN()
        knn_model.load_index(KNN_INDEX_PATH, knn_matrix)

        scaled_features = fit_scale_features(feature_vector, scaler_params)
        scaled_features = np.array(scaled_features, dtype=np.float32)

        print scaled_features
        print knn_params

        indices, dist = knn_model.nn_index(scaled_features,
                                           num_neighbors=4,
                                           checks=knn_params['checks'])
        return zip(indices, dist)

def run():
    nodes, edges, features = read_training_data()
    train_matrix(np.array([map(float, f) for f in features.values()], dtype=np.float32))

