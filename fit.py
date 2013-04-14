#!/usr/bin/python

import pandas as pd
import custom_cv_fit from model

m = pd.read_csv('data/train.csv').as_matrix()
labels = m[:,0]
train = m[:,1:]

print custom_cv_fit(train, labels)
