from watson_developer_cloud import ToneAnalyzerV3
import pickle

ta_credentials ={
  "url": "https://gateway.watsonplatform.net/tone-analyzer/api",
  "username": "feb9c202-fca1-4f64-965a-b72f1259069b",
  "password": "OvcXkqk5kFCV"
}

tone_analyzer = ToneAnalyzerV3(
    username=ta_credentials['username'],
    password=ta_credentials['password'],
   version='2016-05-19')

def make_vectors(text_dict='text_dict3.json', tag='TW08',limit=200):
    # Read JSON file
    import json
    import numpy as np


    count = 0

    with open(text_dict) as data_file:
        text_dict = json.load(data_file)

    y_pre=[]
    X_pre=[]

    for key in text_dict.keys():

        count+= 1

        if tag in text_dict[key]['tags']:
            v = 1

        else:
            v = 0

        print ('Count: {}, key: {}'.format(count,key))

        tone = tone_analyzer.tone(text_dict[key]['text'])
        X_pre.append([tone["document_tone"]["tone_categories"][1]['tones'][0]["score"],
                      tone["document_tone"]["tone_categories"][2]['tones'][4]["score"]])


        y_pre.append([v])

        if count == limit:
            break


    print (len(y_pre))

    print (len(X_pre))


    X = np.array(X_pre)

    y = np.array(y_pre)


    return X, y.ravel(1)


if __name__ == '__main__':


    X, y = make_vectors(tag='TW08', limit=217)

    pickle.dump(X, open("twa_X.p", "wb"))
    pickle.dump(y, open("twa_y.p", "wb"))

    print(X)
    print(y)