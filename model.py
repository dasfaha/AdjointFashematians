from sklearn import metrics
import pandas
import sklearn
import sklearn.svm
import sklearn.decomposition
import sklearn.pipeline
import sklearn.manifold
import sklearn.ensemble
import numpy as np

def build_svm_model(C=1, gamma=0.02, pcomp=39, with_pca=True, **kwargs):
    """Build SVM model with basic parameters """
    clf = sklearn.svm.SVC(C=C, gamma=gamma, probability=False, verbose=True, **kwargs)

    pipeline_elements = [('svc', clf)]

    if with_pca:
       pca = sklearn.decomposition.RandomizedPCA(n_components=pcomp, whiten=True)
       pipeline_elements.append(('pca', pca))

       #scaler = sklearn.preprocessing.StandardScaler(with_std=False)
       #pipeline_elements.append(('scaling', scaler))

    pipeline = sklearn.pipeline.Pipeline(pipeline_elements[::-1])

    return pipeline

def custom_cv_fit(X, y):
    """
    Custom CV code to iterate over parameter grid and compute AUC score
    """

    tuned_parameters = {
      #'pca': [2, 5, 10, 20],
      'C': [1, 10, 100, 1000],
      'gamma': [0.1, 0.01, 0.001, 0.0001],
      'class_weight': ['auto'],
    }

    results = {}

    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    for params in sklearn.grid_search.IterGrid(tuned_parameters):
        print 'Computing with parameters %s\n' % params
        svm = build_svm_model(C=params['C'], gamma=params['gamma'], with_pca=False, # pcomp=params['pca'], with_pca=False,
                              class_weight=params['class_weight'])
        mean_score = sklearn.cross_validation.cross_val_score(svm, X, y,
                            scoring=sklearn.metrics.SCORERS['roc_auc'], cv=2).mean()

        print 'Mean score is %0.5f\n' % mean_score
        results[mean_score] = params

    return results

def make_submission(clf, X_test, file='/tmp/submission.txt'):
    # predict from model
    series = pandas.Series(clf.predict(X_test))
    series.astype(int).tofile(file, sep='\n')


