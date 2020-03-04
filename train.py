import kashgari
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
from sklearn.model_selection import train_test_split
import time

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

train_x, test_x, train_y, test_y = train_test_split(words, labels, test_size=0.5, random_state=50)


bert_embed = BERTEmbedding('uncased_L-12_H-768_A-12',
                           trainable=False,
                           task=kashgari.LABELING,
                           sequence_length=20,
                           )
model = BiLSTM_CRF_Model(bert_embed)
model.fit(train_x,
          train_y,
          x_validate=test_x,
          y_validate=test_y,
          epochs=35,
          batch_size=256)

model.save('model_bilstm_crf_35_256_64')

model.evaluate(x_data=test_x,y_data=test_y,batch_size=64,debug_info=True)