#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
from __future__ import division
#from __future__ import absolute_import


__source__ = "lstm_2_train.py"
__author__ = "Frank J. Greco"
__copyright__ = ""
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = "Frank J. Greco"
__email__ = ""
__status__ = "Development"


from tflearn.data_utils import to_categorical, pad_sequences

import make_twa as twa
import splitXy
import pickle


import lstm_2_model

# Prepare training and test data...

#trainX=[[0,0,0,0,0,0,0,1,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,6,0,0,6,0],[0,0,0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0]]
#trainX.extend(trainX)

#trainY=[1,1,0,1,1,1]
#trainY.extend(trainY)

#testX=[[0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0,0,],[0,0,0,0,0,0,0,1,0,0]]
#testY=[1,1,1]

#X,y = twa.make_vectors(tag='TW08', limit=217)

X = pickle.load(open("twa_X.p", "rb"))
y = pickle.load(open("twa_y.p", "rb"))

trainX, trainY, testX, testY=splitXy.split(X,y,maxlen=300,splitat=100)

m=lstm_2_model.TFModel()

# Define NN model...
model=m.build()

# Training step...
model.fit(trainX, trainY, n_epoch=1,validation_set=(testX, testY), show_metric=True,
          batch_size=3)

# For program testing purposes...
predX = testX

predX = pad_sequences(predX, maxlen=300, value=0.)

pred=model.predict(predX)

with open('lstm_2.log', 'w') as f:
    for i in range(0,len(predX)):
        line='{} {} {} {}'.format("prediction: ", i, pred[i][0],pred[i][1])
        f.write(line+'\n')
        print(line)

# Save weights for later use...
model.save(m.tfl)

