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


train_x1, test_x, train_y1, test_y = train_test_split(words, labels, test_size=0.3, random_state=40)