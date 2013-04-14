#!/usr/bin/python

import pyflann
import cPickle
import math

from graph_analyser import TrainingGraph

import numpy as np

KNN_INDEX_PATH = 'models/knn_index.pk'
KNN_MATRIX_PATH = 'models/knn_matrix.pk'
KNN_PARAMS_PATH = 'models/knn_params.pk'
KNN_SCALER_PARAMS_PATH = 'models/knn_scaler_params.pk'

f = open(KNN_MATRIX_PATH, 'r')
knn_matrix = cPickle.load(f)
f.close()

#print("loading knn model params from %s" % KNN_PARAMS_PATH)
f = open(KNN_PARAMS_PATH, 'r')
knn_params = cPickle.load(f)
f.close()

#print("loading knn scaler params from %s" % KNN_SCALER_PARAMS_PATH)
f = open(KNN_SCALER_PARAMS_PATH, 'r')
scaler_params = cPickle.load(f)
f.close()

#print("loading knn index from %s" % KNN_INDEX_PATH)
knn_model = pyflann.FLANN()
knn_model.load_index(KNN_INDEX_PATH, knn_matrix)

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

    #print('saving knn scaler params to %s' % KNN_SCALER_PARAMS_PATH)
    f = open(KNN_SCALER_PARAMS_PATH, 'w')
    cPickle.dump(scaler_params, f)
    f.close()

    flann = pyflann.FLANN()
    params = flann.build_index(train_matrix,
                               target_precision = 0.95,
                               log_level = 'info',
                               algorithm = 'autotuned')

    #print('saving knn index to %s' % KNN_INDEX_PATH)
    flann.save_index(KNN_INDEX_PATH)

    #print('saving knn matrix to %s' % KNN_MATRIX_PATH)
    f = open(KNN_MATRIX_PATH, 'w')
    cPickle.dump(train_matrix, f)
    f.close()

    #print('saving knn params to %s' % KNN_PARAMS_PATH)
    f = open(KNN_PARAMS_PATH, 'w')
    cPickle.dump(params, f)
    f.close()

def predict(feature_dict):

        features = [feature_dict[k] for k in sorted(feature_dict.keys())]
        features = map(float, features)
        scaled_features = fit_scale_features(features, scaler_params)
        scaled_features = np.array(scaled_features, dtype=np.float32)

        indices, dist = knn_model.nn_index(scaled_features,
                                           num_neighbors=10,
                                           checks=knn_params['checks'])
        return indices

def run():
    tg = TrainingGraph()
    features = [tg.td.node_attr_map[k] for k in sorted(tg.G.nodes())]
    ordered_features = []
    for f in features:
        ordered_features.append([f[fi] for fi in sorted(f, key=f.get)])
    train_matrix(np.array([map(float, f) for f in ordered_features], dtype=np.float32))

