#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "tag_analysis/ipynb"
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__email__ = ""
__status__ = "Development"

#
# tag_analysis.py
#
#Look at the tag sets assigned to pairs of documents and calculates the Jacquard similarity of the tag sets.
#

import collections

import xlrd

from jaccard import jaccard_similarityn

from preprocess import create_tag_dict

def create_countList(td):

    print()
    print ("Running create_countlist()")

    # Create tag pair occurence list
    corrList=[]
    for case in td.keys():
        if len(td[case]) == 1:
            continue
        for y in range(len(td[case])):
            for z in range(y,len(td[case])):

                if td[case][y]< td[case][z]:
                    corrList.append([td[case][y],td[case][z]])
                else:
                    corrList.append([td[case][z], td[case][y]])

    corrList.sort(key=lambda tup: (tup[0],tup[1]))  # This may not be needed


    # Count occurences for each pair of tag values

    currentItem=['na','na']
    currentCount = 0
    countList=[]
    for item in corrList:
        if item != currentItem:
            currentItem.append(currentCount)
            countList.append(currentItem)
            currentItem = item
            currentCount = 1
        else:
            currentCount += 1

    currentItem.append(currentCount)
    countList.append(currentItem)

    del countList[:1] #Remove initialization item

    print()
    print ("Co-occurence Count List: ")
    print()

    #print "Sorted by First Tag: "
    #for item in countList:
    #    print item

    print()
    print ("Sorted by FrequencyPair : ")
    countList.sort(key=lambda x: x[2] )
    countList2 = countList
    countList2.reverse()
    for item in countList2:
        print (item)

    with open(tag_pair_frequency_filename, 'wb') as csvfile:
        for item in countList2:
            if item[0]==item[1]:
                pass
            else:
                csvfile.write('\n'+str(item[0])+','+str(item[1])+','+str(item[2]))

    return countList

######## Table building ##########
def find_x_and_y(array):
    '''Step 1: Get unique x and y coordinates,
    and the width and height of the matrix'''
    x = sorted(list(set([i[0] for i in array])))
    y = sorted(list(set([i[1] for i in array])))

    width = len(x) + 1
    height = len(y) + 1

    #print "width: ", width, "height: ", height

    return x, y, width, height

def construct_initial_matrix(array):
    '''Step 2: Make the initial matrix (filled with zeros)'''
    x, y, width, height = find_x_and_y(array)

    matrix = []
    for i in range(height):
        matrix.append([0] * width)

    return matrix

def add_edging(array, matrix):
    '''Step 3: Add the x and y coordinates to the edges'''
    x, y, width, height = find_x_and_y(array)

    for coord, position in zip(x, range(1, height)):
        matrix[position][0] = coord

    for coord, position in zip(y, range(1, width)):
        matrix[0][position] = coord

    return matrix

def add_z_coordinates(array, matrix):
    '''Step 4: Map the coordinates in the array to the position
    in the matrix'''
    x, y, width, height = find_x_and_y(array)

    x_to_pos = dict(zip(x, range(1, height)))
    y_to_pos = dict(zip(y, range(1, width)))

    for x, y, z in array:
        matrix[x_to_pos[x]][y_to_pos[y]] = z
    return matrix

def make_csv(matrix):
    '''Step 5: Pretty-printing'''

    with open(tag_analysis_matrix_filename, 'wb') as csvfile:
        csvfile.write( '\n'.join(', '.join(str(i) for i in row) for row in matrix))

    return '\n'.join(', '.join(str(i) for i in row) for row in matrix)

def main():

    print
    print ('xls_pathname', xls_pathname)
    print ('jaccard_tag_filename', jaccard_tag_filename)
    print ('tag_analysis_matrix_filename', tag_analysis_matrix_filename)
    print ('tag_pair_frequency_filename', tag_pair_frequency_filename)

    #example = [[1, 1, 10], [1, 2, 11], [2, 1, 12], [2, 2, 13]]
    #example = [[1000,250,12.2],[1000,500,10],[2000,250,15],[2000,500,13.5]]
    #ts, td = analyze_tags(xls_pathname)

    td = create_tag_dict(xls_pathname)

    example = create_countList(td)

    matrix = construct_initial_matrix(example)
    matrix = add_edging(example, matrix)
    matrix = add_z_coordinates(example, matrix)

    print(make_csv(matrix))

    f=open(jaccard_tag_filename,'w')

    for s1 in td:
        for s2 in td:
                if s1 < s2:
                    js=jaccard_similarityn(td[s1],td[s2])
                    #print str(s1),td[s1],str(s2),td[s2],js
                    f.write(','.join([str(s1),'"'+str(','.join(td[s1]))+'"',
                                      str(s2),'"'+str(','.join(td[s2]))+'"',
                                      str(js)])+'\n')

    f.close()

if __name__ == "__main__":
    xls_pathname = '../CC_FILES_TAGLIST/TW Case List.xlsx'
    jaccard_tag_filename="jaccard_tag.csv"
    tag_analysis_matrix_filename='tag_analysis_matrix.csv'
    tag_pair_frequency_filename='tag_pair_frequency.csv'
    main()

