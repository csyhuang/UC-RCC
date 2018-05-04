from __future__ import division, print_function, absolute_import

import tflearn
# -*- coding: utf-8 -*-
"""
Class TFModel is adapted from the following:

Simple example using a Dynamic RNN (LSTM) to classify IMDB sentiment dataset.
Dynamic computation are performed over sequences with variable length.
References:
    - Long Short Term Memory, Sepp Hochreiter & Jurgen Schmidhuber, Neural
    Computation 9(8): 1735-1780, 1997.
    - Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng,
    and Christopher Potts. (2011). Learning Word Vectors for Sentiment
    Analysis. The 49th Annual Meeting of the Association for Computational
    Linguistics (ACL 2011).
Links:
    - http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf
    - http://ai.stanford.edu/~amaas/data/sentiment/
"""

class TFModel:

    def __init__(self):
        self.description = "LSTM 2 Neural Network Model"
        self.author = "F.J. Greco"
        self.tfl = 'lstm_2.tfl'


    def build(self):

        # Network building
        net = tflearn.input_data([None, 300])
        # Masking is not required for embedding, sequence length is computed prior to
        # the embedding op and assigned as 'seq_length' attribute to the returned Tensor.
        net = tflearn.embedding(net, input_dim=300, output_dim=300)
        net = tflearn.lstm(net, 5, dropout=0.1, dynamic=True)
        net = tflearn.fully_connected(net, n_units=2, activation='softmax')
        net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,
                                 loss='categorical_crossentropy')

        # Training
        model = tflearn.DNN(net, tensorboard_verbose=0)
        return model
