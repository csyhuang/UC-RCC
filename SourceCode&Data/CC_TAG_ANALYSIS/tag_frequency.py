# Count tag occurances for curated files

import json
import collections
text_dict='text_dict5.json'
with open(text_dict) as data_file:
    text_dict = json.load(data_file)

count=0
master=[]

for key in text_dict.keys():
    count +=1
    master.extend(text_dict[key]['tags'])

counter=collections.Counter(master)
print (counter)


import csv

with open("tag_counts.csv", "w") as csvFile:
    wr = csv.writer(csvFile, dialect='excel')
    for key in counter.keys():
        print key, counter[key]
        wr.writerow([key, counter[key]])
