import json,codecs

file = open('annotations.txt', 'r', encoding='UTF-8')
js = file.read();
dic = json.loads(js);
list_aOq = dic["annotationsOfQueries"]

def process_date(str):
    strlist = str.split()
    for i in range(len(strlist)):
        if strlist[i][0].isdigit():
            for j in strlist[i]:
                if j == "-":
                    strlist[i] = strlist[i].replace("-", " to ")
                    break
    return " ".join(strlist)

def process_comma(str):
    str = str.replace(",", " ")
    str = str.replace("(", " ")
    str = str.replace(")", " ")
    str = str.replace("/", " ")
    str = str.replace("'s"," ") #University of Washington's 可能会出现这种情况
    return str

#处理有问题
#①，一个词若多次出现，则无法处理
#②，会有I在首位的情况
#③，一个词多个标签the countries of the EU（LOC）【Domain/Topic】
# {"query": "the countries of the EU  take days off annual leave  dates", "annotations": [{"category": "B-Geospatial", "value": "EU"}, {"category": "B-Concept", "value": "dates"}, {"category": "B-Domain/Topic", "value": "countries"}, {"category": "I-Domain/Topic", "value": "of"}, {"category": "I-Domain/Topic", "value": "the"}, {"category": "I-Domain/Topic", "value": "EU"}, {"category": "B-Concept", "value": "annual"}, {"category": "I-Concept", "value": "leave"}]}
for lv in list_aOq:

#大小写保持，因为name一般都是大写
    lv["query"] = process_date(lv["query"])
    lv["query"] = process_comma(lv["query"])
    lv["query"] = lv["query"]

    for an in lv["annotations"][:]:

        valuelist = an["value"].split(" ") #value、query全部小写

        if len(valuelist)>1:
            for i in range(len(valuelist)):
                if i==0:
                    dict1 = {'category': "B-"+an["category"] ,'value':valuelist[i]}
                    lv["annotations"].append(dict1)

                else:
                    dict1 = {'category':"I-"+an["category"] ,'value':valuelist[i]}
                    lv["annotations"].append(dict1)

            lv["annotations"].remove(an)
        else:
            an["category"] = "B-" + an["category"]




dic_out = {'annotationsOfQueries':list_aOq}
jsObj = json.dumps(dic_out)
fileObject = open('jsonFile.json', 'w')
fileObject.write(jsObj)
fileObject.close()


#生成两个txt
def saveData():
    file = open('jsonFile.json', 'r', encoding='UTF-8')
    js = file.read();
    dic = json.loads(js);
    list_aOq = dic["annotationsOfQueries"]

    train_x_file = open('data.txt', 'a')
    train_y_file = open("label.txt", 'a')

    for lv in list_aOq:  # lv是一个个小的dict   {"query":……,"annotations":……}
        str_x = ''
        str_y = ''

        querylist = lv["query"].split()  # query
        for i in range(len(querylist)):

            flag = 0;
            for an in lv["annotations"]:
                valuelist = an["value"].split(" ")
                value_length = len(valuelist)

                if querylist[i] == an["value"]:
                    flag = 1
                    if an["category"] == "B-Data Format":  # category可能是data format，词组不行！！！！！！
                        str_y += "B-DataFormat" + " "
                    elif an["category"] == "I-Data Format":  # category可能是data format，词组不行！！！！！！
                        str_y += "I-DataFormat" + " "
                    elif an["category"] == "Data Format":  # category可能是data format，词组不行！！！！！！
                        str_y += "B-DataFormat" + " "

                    elif an["category"] == "Other Entities":
                        str_y += "B-OtherEntities" + " "
                    elif an["category"] == "B-Other Entities":
                        str_y += "B-OtherEntities" + " "
                    elif an["category"] == "I-Other Entities":
                        str_y += "I-OtherEntities" + " "

                    elif an["category"] == "Other Numbers":
                        str_y += "B-OtherNumbers" + " "
                    elif an["category"] == "B-Other Numbers":
                        str_y += "B-OtherNumbers" + " "
                    elif an["category"] == "I-Other Numbers":
                        str_y += "I-OtherNumbers" + " "
                    else:
                        str_y += an["category"] + " "
                    str_x += querylist[i] + " "
                    break;
            if flag == 0:
                str_y += "other" + " "
                str_x += querylist[i] + " "

        str_y.strip('')
        str_x.strip('')
        str_x += "\n"
        str_y += "\n"

        train_x_file.write(str_x)
        train_y_file.write(str_y)

saveData()