def pairwise_transform(X, f=lambda x: x):
    return f(X[:, :11]) - f(X[:, 11:])
