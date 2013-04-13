import numpy as np

from scipy.cluster.vq import kmeans2
from scipy import ndimage as ndi

from sklearn.cross_validation import train_test_split

def pairwise_transform(X, f=lambda x: x):
    return f(X[:, :11]) - f(X[:, 11:])

def ensemble(estimators, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    y_preds = np.zeros((len(estimators), len(y_test)))

    for i,est in enumerate(estimators):
        print 'Fitting ', i
        est.fit(X_train, y_train)
        print 'Predicting ', i
        y_preds[i] = est.predict_proba(X_test)[:, 1]

    preds = np.vstack(y_preds)
    y_pred_avg = np.average(preds.T, axis=1)

    return y_test, y_pred_avg, y_preds
