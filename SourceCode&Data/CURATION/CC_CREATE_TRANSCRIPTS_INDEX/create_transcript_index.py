#!/usr/bin/env python

__source__ = 'cc_transcript_index.py'
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

#
# Create a csv file with the following fields: index,caseID,filename
#

import os, re

def main(transcript_dir, transcript_index):

    print
    print 'transcript_dir:',transcript_dir
    print 'transcript_index:',transcript_index
    print

    doc_index=[]

    index=0

    fo=open(transcript_index,'w')

    fo.write('{},{},{}\n'.format('index','caseID','filename'))

    for filename in os.listdir(transcript_dir):

        if filename.endswith(".txt"):
            name_tokens = filename.split()

            s = re.sub('[^0-9]+', ' ', name_tokens[2])

            infile = transcript_dir + '/' + filename

            doc_index.append((index,s,filename))

            fo.write('{},{},{}\n'.format(index,s,filename))
            index += 1

    fo.close

if __name__ == "__main__":
    main(transcript_dir = '../CC_TRANSCRIPTS',
         transcript_index='transcript_index.csv')