from tflearn.data_utils import to_categorical, pad_sequences

def split(X, y, maxlen=300, splitat=100):
    trainX = X[:splitat]
    trainY = y[:splitat]

    testX = X[splitat:]
    testY = y[splitat:]

    # Data preprocessing
    # NOTE: Padding is required for dimension consistency. This will pad sequences
    # with 0 at the end, until it reaches the max sequence length. 0 is used as a
    # masking value by dynamic RNNs in TFLearn; a sequence length will be
    # retrieved by counting non zero elements in a sequence. Then dynamic RNN step
    # computation is performed according to that length.

    trainX = pad_sequences(trainX, maxlen=maxlen, value=0.)
    testX = pad_sequences(testX, maxlen=maxlen, value=0.)

    # Converting labels to binary vectors
    trainY = to_categorical(trainY, nb_classes=2)
    testY = to_categorical(testY, nb_classes=2)

    return trainX, trainY, testX, testY