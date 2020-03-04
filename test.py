import kashgari,numpy as np
import time
from sklearn.model_selection import train_test_split

datafile = open('data.txt', 'r')
labelfile = open('label.txt', 'r')

words, labels = [], []

count = 0
for data, label in zip(datafile, labelfile):
    count += 1
    s1 = data.strip().split(' ')
    s2 = label.strip().split(' ')

    words.append(s1)
    labels.append(s2)

# print("words:")
# print(words)
# print("labels:")
# print(labels)
train_x, test_x, train_y, test_y = train_test_split(words, labels, test_size=0.5, random_state=50)

test_1 = "user behavior data from video"

test_ = []
test_.append(test_1.split())

start1 = time.clock()
loaded_model = kashgari.utils.load_model('model_bilstm_crf_30_256')
# loaded_model.evaluate(x_data=test_x,y_data=test_y,batch_size=64,debug_info=True)
# start = time.clock()
#
result = loaded_model.predict(test_)
print(result)
# end = time.clock()
#
# print("加载模型时间：%f",start-start1)
#
# print("predict时间：%f",end-start)





# test_.append(test_2.split())
# test_.append(test_3.split())
# test_.append(test_4.split())
# test_.append(test_5.split())
# test_.append(test_6.split())
# test_.append(test_7.split())
# test_.append(test_8.split())
# test_.append(test_9.split())
