import kashgari
from mapping_test import disting_format, disting_lang
from stanfordcorenlp import StanfordCoreNLP
'''
def pro_lang_format 词表处理language和DataFormat
def pro_geo_tem   用coreNLP处理Temporal和Geospatial
def pro_meta_content  处理其他label
'''
#metadata&content标签，用BIO标注
part_meta = ["B-Language", "B-Accessibility", "B-Provenance", "I-Provenance", "I-Language",
             "B-Statistics", "B-Domain/Topic", "I-Domain/Topic", "B-Name", "I-Name", "I-DataFormat", "B-DataFormat",
             "I-Statistics"]

part_content = ["B-Concept", "I-Concept", "B-Geospatial", "I-Geospatial", "B-Temporal", "I-Temporal", "B-OtherNumbers",
                "I-OtherNumbers", "B-OtherEntities", "I-OtherEntities"]

#输出结果，每一类一个list
dict_result = {'metadata': {}, 'content': {}}

#处理language和dataformat【预定义词表】
#language词表只有常用语言
#dataformat只有部分格式，可继续扩展
def pro_lang_format(text):
    '''

    :param text: list
    :return: 
    '''

    global dict_result

    lang = disting_lang(text)

    if len(lang) > 0:
        dict_result['metadata']['Language'] = lang

    data_format = disting_format(text)

    if len(data_format) > 0:
        dict_result['metadata']['DataFormat'] = data_format
#Bert-Bilstm-CRF模型处理标记
def pro_meta_content(test1_list):
    '''

    :param test1_list: [] 格式
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


    i = 0
    while i < len(result):

        if result[i] in part_content:  #若该词属于content
            tmp = []  #tmp暂存，因为识别的结果可能是[B-Concept I-Concept I-Concept]
            tmp.append(test1_list[i])
            str = " ".join(tmp)  # value
            type = result[i][2:]
            i = i + 1


            while i < len(result):
                if result[i][0] == 'I':

                    tmp.append(test1_list[i])
                    str = " ".join(tmp)
                    type = result[i][2:]
                    i = i + 1
                else:
                    break

            if dict_result['content'].get(type) == None:
                dict_result['content'][type] = [str]
            else:
                if str not in dict_result['content'][type]:  #词表和corenlp和bilstm-crf识别取并集
                    dict_result['content'][type].append(str)

        #该类别为metadata
        elif result[i] in part_meta:
            tmp = []
            tmp.append(test1_list[i])
            str = " ".join(tmp)  # value
            type = result[i][2:]

            i = i + 1


            while i < len(result):
                if result[i][0] == 'I':

                    tmp.append(test1_list[i])

                    str = " ".join(tmp)
                    type = result[i][2:]  # 可能出错，只有B，没有I的话！！！！！！！！！！！！！！！！！

                    i = i + 1
                else:
                    break



            if dict_result['metadata'].get(type) == None:
                dict_result['metadata'][type] = [str]
            else:
                if str not in dict_result['metadata'][type]:
                    dict_result['metadata'][type].append(str)

        #无关词other
        else:
            i = i + 1
#用corenlp识别Temporal和Geospatial
def pro_geo_tem(test_1):
    '''
    :param test_1: str类型
    :return: 
    '''

    global dict_result

    #加载模型【耗时长】
    en_model = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27', lang='en')
    temAndgeo = en_model.ner(test_1)

    print("temAndgeo:", temAndgeo)

    i = 0
    while i < len(temAndgeo):
        if temAndgeo[i][1] == "DATE":
            tmp = []
            while i < len(temAndgeo):
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
        # duration 和date 暂时都视作Temporal
        elif temAndgeo[i][1] == "DURATION":
            tmp = []
            while i < len(temAndgeo):
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
        #识别Geospatial，corenlp识别比较细
        elif temAndgeo[i][1] == ("COUNTRY" or "ORGANIZATION" or "LOCATION" or "CITY" or "STATE_OR_PROVINCE"):  # EU会被识别成organization
            if dict_result['content'].get('Geospatial') == None:
                dict_result['content']['Geospatial'] = [temAndgeo[i][0]]
            else:
                if temAndgeo[i][0] not in dict_result['content']['Geospatial']:
                    dict_result['content']['Geospatial'].append(temAndgeo[i][0])

            i = i + 1
        else:
            i = i + 1


##############输入str
test_1 = "NTU-HD dataset,a hand gesture dataset,color image and the corresponding depth map"
test_1 = test_1.replace(",", " ")
test1_list = test_1.split()

# 处理Language和DataFormat
pro_lang_format(test1_list)
# 处理Geospatial和Temporal
pro_geo_tem(test_1)
# 处理其他
pro_meta_content(test1_list)


#打印结果
# 【eg：dict_result: {'metadata': {'DataFormat': ['image'], 'Domain/Topic': ['hand gesture']}, 'content': {'Concept': ['corresponding depth map']}}
print("dict_result:", dict_result)

#有可能出现query太短/query本身无意义 等情况，导致无法识别任一label  →  整体在metadata中搜索？
