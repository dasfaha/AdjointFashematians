import pandas

def load_data(file):
    return pandas.read_csv(file).as_matrix()

train = load_data('./data/train.csv')
test = load_data('./data/test.csv')

labels = train[:, 0]
train = train[:, 1:]





