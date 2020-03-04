
metadata = ["Name", "Domain/Topic", "Data+Format", "Language", "Accessibility", "Provenance",
            "Statistics","B-Domain/Topic","I-Domain/Topic","B-Name","I-Name","I-Data+Format","B-Data+Format",
            "B-Accessibility", "I-Accessibility", "B-Statistics",
           "I-Statistics", "B-Provenance", "I-Provenance"]

content = ["Concept", "Geospatial", "Other+Entities", "Temporal", "Other+Numbers","B-Concept",
            "I-Concept","B-Other+Entities","I-Other+Entities","B-Geospatial","I-Geospatial",
            "B-Temporal","I-Temporal","B-Other+Numbers","I-Other+Numbers"]

labelfile = open('label.txt', 'r')

savefile = open('label2.txt','a')
# labels = []

count = 0
for label in labelfile:
    s2 = label.strip().split(' ')

    tmp= []
    for x in s2:
        if x in metadata:
            if x[0] == 'B':
                tmp.append('B-MTD')
            elif x[0] == 'I':
                tmp.append('I-MTD')
            else:
                tmp.append('MTD')
        elif x in content:
            if x[0] == 'B':
                tmp.append('B-CTT')
            elif x[0] == 'I':
                tmp.append('I-CTT')
            else:
                tmp.append('CTT')
        else:
            tmp.append('OTR')

    savefile.write(' '.join(tmp)+'\n')

    # labels.append(tmp)

