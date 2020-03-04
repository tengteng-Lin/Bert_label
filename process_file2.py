import json

LABEL = ["B-Language","I-Language","B-Domain/Topic","I-Domain/Topic",
               "B-Name","I-Name","I-DataFormat","B-DataFormat","B-Concept",
               "I-Concept", "B-Geospatial", "I-Geospatial", "B-Temporal", "I-Temporal", "B-OtherNumbers",
               "I-OtherNumbers", "B-OtherEntities", "I-OtherEntities", "B-Accessibility", "I-Accessibility",
               "B-Statistics","I-Statistics", "B-Provenance", "I-Provenance"]

train_x_file = open('data.txt', 'a')
train_y_file = open("label.txt", 'a')

file = open('annotations2.txt', 'r', encoding='UTF-8')
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
    str = str.replace("'s", " ")  # University of Washington's 可能会出现这种情况
    return str
#先存储data
for lv in list_aOq:
    # 处理日期和特殊符号，干扰标注
    lv["query"] = process_date(lv["query"])
    lv["query"] = process_comma(lv["query"])


    lv['query'] = lv['query'].strip('')
    train_x_file.write(lv['query']+'\n')


#标注变形【（students marks，Domain/Topic） → （students marks，Domain/Topic-B，Domain/Topic-I）】
for lv in list_aOq:
    #处理日期和特殊符号，干扰标注
    lv["query"] = process_date(lv["query"])
    lv["query"] = process_comma(lv["query"])

    for an in lv['annotations']:
        valuelist = an['value'].split()

        an['category'] = an['category'].replace(" ",'')

        tmpCate = []
        for i in range(len(valuelist)):
            if i==0:
                tmpCate.append("B-"+an['category'])
            else:
                tmpCate.append("I-"+an['category'])
        an['category'] = ' '.join(tmpCate)
        # print(an['category'])

#标注替换query
for lv in list_aOq:
    for an in lv['annotations']:
        lv['query'] = lv['query'].replace(an['value']," "+an['category']+" ")

    # print("①"+lv['query'])
    querylist = lv['query'].split()
    # print(querylist)
    for q in querylist[:]:
        # print("q:",q)
        if q not in LABEL:
            idx = querylist.index(q)
            querylist.remove(q)
            querylist.insert(idx,'other')

            # lv['query'] = lv['query'].replace(q,"other")
            # print(querylist)
    lv['query'] = ' '.join(querylist)
    lv['query'] = lv['query'].strip('')
    train_y_file.write(lv['query']+'\n')
    # print("②"+lv['query']+"\n")

dic_out = {'annotationsOfQueries':list_aOq}
jsObj = json.dumps(dic_out)
fileObject = open('allCate.json', 'w')
fileObject.write(jsObj)
fileObject.close()


