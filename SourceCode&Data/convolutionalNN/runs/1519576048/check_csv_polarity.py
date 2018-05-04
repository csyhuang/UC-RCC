POS2=0
NEG2=0

for line in open('prediction.csv'):
        x=line.split(',')

        if "1" in x[1] :
            POS2 += 1
        else:
            NEG2 += 1


print ('POS2', POS2, 'NEG2', NEG2)