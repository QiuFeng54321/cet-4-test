import unicodedata
import re
import requests
import json
import io
from urllib import parse

english = 'D:\\USB-WILLIAM\\Learn\\新东方四级词汇乱序版.txt'

exclude = ['超纲单词表', '熟词僻义表', '的']
zhmodel = re.compile(u'[\u4e00-\u9fa5]')

with open(english, 'r', encoding='utf-8') as file:
    u = file.read()
str_list = u.split("\n")
for str_i in range(len(str_list)):
    str_list[str_i] = "".join(ch for ch in str_list[str_i] if unicodedata.category(ch)[0] != "C").strip()
str_list = list(filter(str.strip, str_list))
str_list = list(filter(lambda x: not x in exclude, str_list))
str_list = list(filter(lambda x: not x.isnumeric(), str_list))
to_be_searched_i = []
to_be_searched = []
chunk = []
counter = 0
length = 0
for str_i in range(len(str_list)):
    str_list[str_i] = [str_list[str_i].split(" ")[0]]

    if zhmodel.match(str_list[str_i][0]):
        continue
    to_be_searched_i.append(str_i)
    chunk.append(str_list[str_i][0])
    counter += 1
    length += 1
    if counter >= 20:
        counter = 0
        to_be_searched.append(chunk)
        chunk = []
if counter > 0:
    to_be_searched.append(chunk)
res = []
index = 0
for chunk in to_be_searched:
    print(length - index, "Left.", "Chunk:", chunk)
    while True:
        try:
            x = requests.post("https://definition.williamcraft.workers.dev/", timeout=20,
                              data=json.dumps(chunk))
            text = x.text
            x = json.loads(text)
            for i in range(len(x)):
                actual_i = to_be_searched_i[index + i]
                str_list[actual_i].append(x[i])
            break
        except Exception as e:
            print(e)
            print("Try again...")
            pass


    res += x
    index += 20
# order = 0
# for i in to_be_searched_i:
#     str_list[i].append(res[order])
#     order += 1

f = io.open("out.txt", "w")
f.write(json.dumps(str_list))
f.close()
