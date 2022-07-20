import csv
import requests
import csv
import re
import json

t1 = []  # 存储处理前的标题
t_list = []  # 存储处理后的标题
c_list = []  # 存储正文内容
# 从csv文件里把标题+正文读取到数组里，记得将该文件和上述csv文件放到通过文件目录下，否则需要加相对路径
with open("corpus.csv", "r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        t_list.append(row[0])
        c_list.append(row[1])
        t1.append(row[0])
# 处理标题里的空格，括号
for i in range(len(t_list)):
    t_list[i] = t_list[i].replace(' ', '_')
    t_list[i] = t_list[i].replace('(', '')
    t_list[i] = t_list[i].replace(')', '')
    while t_list[i][-1] == '_':
        t_list[i] = t_list[i][0:-1]

for i in range(len(c_list)):
    c_list[i] = c_list[i].replace("\"", '')
    c_list[i] = c_list[i].replace('?', ' ')
    c_list[i] = c_list[i].replace('\n', ' ')

# delete duplicated information
d1=dict(zip(t_list,c_list))

headers = {
	"X-RapidAPI-Key": "477b42042fmsh1436202cccff4e6p113600jsn90a00cfda59b",
	"X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
}
def fetch_synonyms(word):

  url = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/synonyms"
  api_response = requests.request("GET", url, headers=headers)

  return json.loads(api_response.text)



with open("domain.yml", "w", newline="", encoding="utf-8") as f:
    f.write('version: "2.0"' + '\n')
    f.write('\n')
    f.write('intents:' + '\n')
    for k in d1.keys():
        f.write('  - ' + k + '\n')

    f.write('\n')
    f.write('responses:' + '\n')
    for k,v in d1.items():
        f.write('  '+'utter_' + k + ':\n')
        f.write('  ' + '- text: "' + v + '"\n')
        f.write('\n')

    f.write('\n')
    f.write('session_config:' + '\n')
    f.write('  session_expiration_time: 60' + '\n')
    f.write('  carry_over_slots_to_new_session: true' + '\n')

with open("nlu.yml", "w", newline="", encoding="utf-8") as f:
    f.write('version: "2.0"' + '\n')
    f.write('\n')
    f.write('nlu:' + '\n')
    for i in range(len(t_list)):
        f.write('- intent: ' + t_list[i] + '\n')
        f.write('  examples: |\n')
        f.write('   - ' + t1[i] + '\n')
        f.write('   - ' + t1[i].lower() + '\n')
        f.write('   - ' + t1[i].upper() + '\n')
        if(len(t1[i].split()) >= 3 and '(' in t1[i] ):
            response = fetch_synonyms(t1[i].split()[0])
            if("synonyms" in response):
                for w in response["synonyms"]:
                    f.write('   - ' + w + '\n')
        elif(len(t1[i].split()) == 1 ):
            response = fetch_synonyms(t1[i])
            if("synonyms" in response):
                for w in response["synonyms"]:
                    f.write('   - ' + w + '\n')
        elif(len(t1[i].split()) >= 3 and 'and' in t1[i] ):
            response = fetch_synonyms(t1[i].split()[0])
            if("synonyms" in response):
                for w in response["synonyms"]:
                    f.write('   - ' + w + '\n')
        if(len(t1[i].split()) == 3 and 'and' in t1[i] ):
            response = fetch_synonyms(t1[i].split()[2])
            if("synonyms" in response):
                for w in response["synonyms"]:
                    f.write('   - ' + w + '\n')
        f.write('\n')







with open("rules.yml", "w", newline="", encoding="utf-8") as f:
    f.write('version: "2.0"' + '\n')
    f.write('\n')
    f.write('rules:' + '\n')
    f.write('\n')
    for k,v in d1.items():
#     for i in range(len(t_list)):
        f.write('- rule: ' + k+ '\n')
        f.write('  steps:' + '\n')
        f.write('  - intent: ' + k + '\n')
        f.write('  - action: ' + 'utter_' + k + '\n')
        f.write('\n')

with open("stories.yml", "w", newline="", encoding="utf-8") as f:
    f.write('version: "2.0"' + '\n')
    f.write('\n')
    f.write('stories:' + '\n')
    f.write('\n')
    for k,v in d1.items():
#     for i in range(len(t_list)):
        f.write('- story: ' + k+ '\n')
        f.write('  steps:' + '\n')
        f.write('  - intent: ' + k + '\n')
        f.write('  - action: ' + 'utter_' + k + '\n')
        f.write('\n')