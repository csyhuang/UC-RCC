#Predictive run...

from __future__ import division, print_function, absolute_import

from tflearn.data_utils import to_categorical, pad_sequences

import lstm_2_model
import pickle
import splitXy

#Prepare source data...

testX=[[0,0,0,0,0,0,0,1,0,0,],[0,0,0,0,0,0,0,0,0,2],[2,0,0,0,0,0,0,0,0,0],[0,0,0,0,6,0,0,6,0]]
#testY=[0,1,1,1]

X = pickle.load(open("twa_X.p", "rb"))
y = pickle.load(open("twa_y.p", "rb"))

predX, trainY, testX, testY=splitXy.split(X,y,maxlen=300,splitat=5)

m=lstm_2_model.TFModel()

model=m.build()

#Retrieve weights from training run...
model.load(m.tfl)

# Run against trained model...
pred = model.predict(predX)

for i in range(0,len(predX)):
    print("prediction: ", i, pred[i][1])

