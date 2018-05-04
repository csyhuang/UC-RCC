
POS_Train = sum(1 for line in open('train_pos.txt'))
NEG_Train = sum(1 for line in open('train_neg.txt'))
POS_Test = sum(1 for line in open('test_pos.txt'))
NEG_Test = sum(1 for line in open('test_neg.txt'))

print ('POS_Train', POS_Train, 'NEG_Train', NEG_Train)
print ('POS_Test', POS_Test, 'NEG_Test', NEG_Test)




