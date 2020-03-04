import kashgari
from mapping_test import disting_format,disting_lang
from stanfordcorenlp import StanfordCoreNLP

part_meta = ["B-Language", "B-Accessibility", "B-Provenance","I-Provenance","I-Language",
            "B-Statistics","B-Domain/Topic","I-Domain/Topic","B-Name","I-Name","I-DataFormat","B-DataFormat","I-Statistics"]

part_content = ["B-Concept","I-Concept","B-Geospatial","I-Geospatial","B-Temporal","I-Temporal","B-OtherNumbers",
                "I-OtherNumbers","B-OtherEntities","I-OtherEntities"]

#每个类别应该是一个list
dict_result = {'metadata':{},'content':{}}

def pro_lang_format(text):
    '''
    
    :param text: list
    :return: 
    '''

    global dict_result

    lang = disting_lang(text)

    if len(lang)>0:
        dict_result['metadata']['Language'] = lang

    data_format = disting_format(text)

    if len(data_format)>0:
        dict_result['metadata']['DataFormat'] = data_format

def pro_meta_content(test1_list):
    '''
    
    :param test1_list: 
    :return: 
    '''
    global dict_result
    # global metadata

    test_input = []
    test_input.append(test1_list)

    #加载模型【耗时长】
    loaded_model = kashgari.utils.load_model('model_bilstm_crf_35_256_64')
    result1 = loaded_model.predict(test_input)
    result = result1[0]
    print(result)

    i=0
    while i < len(result):

        if result[i] in part_content:  # 如果是content
            if result[i][0] == 'B':  # 首字母是B，往后遍历

                tmp = []
                tmp.append(test1_list[i])
                i = i + 1

                str="";
                type="";
                while i < len(result) :
                    if result[i][0] == 'I':
                        # print("result[i][0] == 'I':", result[i])
                        tmp.append(test1_list[i])
                        str = " ".join(tmp)  # value
                        type = result[i][2:]
                        i = i + 1
                    else:
                        break

                if dict_result['content'].get(type)==None:
                    dict_result['content'][type] = [str]
                else:
                    dict_result['content'][type].append(str)

            else:

                if dict_result['content'].get(result[i])==None:
                    dict_result['content'][result[i]] = [test1_list[i]]
                else:
                    if test1_list[i] not in dict_result['content'][result[i]]:
                        dict_result['content'][result[i]].append(test1_list[i])


                i=i+1

        elif result[i] in part_meta:


            if result[i][0] == 'B':  # 首字母是B，往后遍历
                # print("result[i][0] == 'B':",result[i])
                tmp = []
                tmp.append(test1_list[i])
                i = i + 1

                str = "";type=""
                while i < len(result) :
                    if result[i][0] == 'I':
                        print("result[i][0] == 'I':", result[i])
                        tmp.append(test1_list[i])

                        str = " ".join(tmp)
                        type = result[i ][2:]  # 可能出错，只有B，没有I的话！！！！！！！！！！！！！！！！！

                        i = i + 1
                    else:
                        break


                print("type:",type)

                if dict_result['metadata'].get(type)== None:
                    dict_result['metadata'][type] = [str]
                else:
                    if str not in dict_result['metadata'][type]:
                        dict_result['metadata'][type].append(str)
                    # print("metadata:", metadata)
            else:
                if dict_result['metadata'].get(result[i])== None:
                    dict_result['metadata'][result[i]] = [test1_list[i]]
                else:
                    if test1_list[i] not in dict_result['metadata'][result[i]]:
                        dict_result['metadata'][result[i]].append(test1_list[i])

                i=i+1

        else:
            i=i+1


def pro_geo_tem(test_1):
    '''
    beginning in April 2009, 5 years  并不好整，5years会被识别为DURATION
    :param test_1: 
    :return: 
    '''

    global dict_result

    en_model = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27', lang='en')
    temAndgeo = en_model.ner(test_1)

    print("temAndgeo:",temAndgeo)

    i=0
    while i<len(temAndgeo):

        if temAndgeo[i][1] == "DATE":
            tmp = []
            while i<len(temAndgeo):
                if temAndgeo[i][1] == "DATE":
                    tmp.append(temAndgeo[i][0])
                    i = i + 1
                else:
                    break

            value = " ".join(tmp)
            if dict_result['content'].get('Temporal') == None:
                dict_result['content']['Temporal'] = [value]
            else:
                if value not in dict_result['content']['Temporal']:
                    dict_result['content']['Temporal'].append(value)
        #duration 和date一起处理成一种格式
        elif temAndgeo[i][1] == "DURATION":
            tmp = []
            while i<len(temAndgeo):
                if temAndgeo[i][1] == "DURATION":
                    tmp.append(temAndgeo[i][0])
                    i = i + 1
                else:
                    break

            value = " ".join(tmp)
            if dict_result['content'].get('Temporal') == None:
                dict_result['content']['Temporal'] = [value]
            else:
                if value not in dict_result['content']['Temporal']:
                    dict_result['content']['Temporal'].append(value)

        elif temAndgeo[i][1] == ("COUNTRY" or "ORGANIZATION" or "LOCATION" or "CITY" or "STATE_OR_PROVINCE"): #EU会被识别成organization

            if dict_result['content'].get('Geospatial') == None:
                dict_result['content']['Geospatial'] = [temAndgeo[i][0]]
            else:
                if temAndgeo[i][0] not in dict_result['content']['Geospatial']:
                    dict_result['content']['Geospatial'].append(temAndgeo[i][0])

            i = i+1

        else:
            i=i+1

test_1 = "Rainfall amounts in West Street Glasgow from April 2007 to September the following year"
test_1 = test_1.replace(","," ").lower() #因为训练时训练集都转化成小写，去除了，
test1_list = test_1.split()


#处理语言和数据格式
pro_lang_format(test1_list)
print(dict_result['metadata'])
print(dict_result['content'])
print("================================================================================")
#处理Geospatial和Temporal
pro_geo_tem(test_1)
print(dict_result['metadata'])
print(dict_result['content'])
print("================================================================================")
#处理其他
pro_meta_content(test1_list)
print("================================================================================")


#如何处理metadata和content都为空的情况
print("dict_result:",dict_result)
