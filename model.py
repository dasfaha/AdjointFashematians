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
    clf = sklearn.svm.SVC(C=C, gamma=gamma, probability=True, verbose=True, **kwargs)

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
      #'C': [1, 10, 100, 1000],
      #'gamma': [0.1, 0.01, 0.001, 0.0001],
      #'class_weight': ['auto'],
      'estimators': [500, 400, 200],
      'subsample': [1.0, 0.80, 0.75],
      'learning_rate': [0.1]
    }

    results = {}

    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    for params in sklearn.grid_search.IterGrid(tuned_parameters):
        print 'Computing with parameters %s\n' % params
        #svm = build_svm_model(C=params['C'], gamma=params['gamma'], with_pca=False, #pcomp=params['pca'], 
        #                      class_weight=params['class_weight'])
        gbm = build_gbm_model(
                n_estimators=params['estimators'], 
                subsample=params['subsample'], 
                learning_rate=params['learning_rate'], with_pca=False)

        mean_score = sklearn.cross_validation.cross_val_score(gbm, X, y,
                            scoring=sklearn.metrics.SCORERS['roc_auc'], cv=5).mean()

        print 'Mean score is %0.5f\n' % mean_score
        results[mean_score] = params

    return results

def build_gbm_model(n_estimators=100, learning_rate=0.1, pcomp=80, subsample=1.0, loss='deviance', with_pca=False):
    clf = sklearn.ensemble.GradientBoostingClassifier(
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            subsample=subsample,
            loss=loss)

    pipeline_elements = [('gbm', clf)]

    if with_pca:
       pca = sklearn.decomposition.RandomizedPCA(n_components=pcomp, whiten=False)
       pipeline_elements.append(('pca', pca))       

    pipeline = sklearn.pipeline.Pipeline(pipeline_elements[::-1])

    return pipeline

def build_extratrees_model(n_estimators=100, learning_rate=0.1, pcomp=90, with_pca=False):
    """Build SVM model with basic parameters """
    clf = sklearn.ensemble.ExtraTreesClassifier(n_estimators=n_estimators,
                              n_jobs=2, bootstrap=True, criterion='entropy',
                              random_state=0)
    pipeline_elements = [('svc', clf)]

    if with_pca:
       pca = sklearn.decomposition.RandomizedPCA(n_components=pcomp, whiten=False)
       pipeline_elements.append(('pca', pca))       

    pipeline = sklearn.pipeline.Pipeline(pipeline_elements[::-1])

    return pipeline


def make_submission(clf, X_test, file='/tmp/submission.txt'):
    # predict from model
    series = pandas.Series(clf.predict_proba(X_test)[:, 1])
    series.astype(float).tofile(file, sep='\n')


