import pandas
import numpy as np

def load_data(file):
    return pandas.read_csv(file).as_matrix()

train = load_data('./data/train.csv')
test = load_data('./data/test.csv')

labels = train[:, 0]
train = train[:, 1:]

train_enriched = load_data('./data/enriched_training.csv')
test_enriched = load_data('./data/enriched_test.csv')

labels_enriched = train_enriched[:, 0]
train_enriched = train_enriched[:, 1:]
test_enriched = test_enriched[:, 1:]

### extract graph features from enriched set
extra_features = np.hstack((train_enriched[:, 11:15], train_enriched[:,26:]))
extra_features_test = np.hstack((test_enriched[:, 11:15], test_enriched[:,26:]))






