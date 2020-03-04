
#统一大小写的问题
languages = ["English","Chinese","French","German","Russian","Japanese","Spanish"]
# accessibilities = ["open","public","private"] #这个很可能在content中出现 暂时不这么处理

#需处理大小写和单复数  satellite/aerial imagery这类的也需要处理
formats = ["jpg",'csv',"websites","website","table","tables","mysql","thermal imaging","image","text",
           "fulltext","wikipedia","photos","photo","star schema","snowflake","sql","videos","video",
           "images","digital photographs","imageJ","curves","curve","Geojson","TSV","pdf","graph",
           "textformat","raw text","tweets","gifs","gif","aerial imagery","satellite imagery","textual",
           "Aerial Images","pictures","picture","kml","xlsx","symbolic form","MIDI","MusicXML","voice",
           "blogs","new articles","wikipedia articles","list","database","digital","lists","geo-json",
           "camera images","graphs","figures"]

#languages也可能出现在content中，但暂时不考虑
#识别语言，输入为list
def disting_lang(text):
    '''
    :param text: list
    :return: string 出现的语言
    '''

    result = []
    for t in text:
        if t in languages:

            result.append(t)
    return result


def disting_format(text):
    '''
    :param text: list
    :return: format那个单词
    '''
    result = []
    for t in text:
        if t in formats:
            result.append(t)
    return result
