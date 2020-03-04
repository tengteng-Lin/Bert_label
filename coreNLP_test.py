from stanfordcorenlp import StanfordCoreNLP
import time

time1 = time.clock()
en_model = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27', lang='en')
time2 = time.clock()

#并不需要识别地特别精确？
#NUTS是识别不出来的，识别不出来的怎么办？
en_sentence = 'weekly temperature measurements, Anchorage Alaska, beginning in April 2009, 5 years'


print ('Named Entities:', en_model.ner(en_sentence))
time3 = time.clock()

print("加载模型时间：%f" ,time2-time1)
print("识别时间：%f" , time3 - time2)