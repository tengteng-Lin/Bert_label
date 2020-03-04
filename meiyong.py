
result = {'metadata':{},'content':{}}

lang = 'France'
type = 'languages'

result['metadata'][type] = [lang]

lang2 = 'CN'
result['metadata'][type].append(lang2)

if result['metadata'].get('Name') == None:
    result['metadata']['Name'] = [lang2]
print(result)