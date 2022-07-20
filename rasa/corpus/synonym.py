import requests
import csv
import re
import json
# create an array to store the words we need
# t_list=[]
# words = []
# with open("corpus.csv", "r",newline="") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         t_list.append(row[0])
#
# for i in t_list:
#
#     if(len(i.split()) == 1 and '(' not in i ):
#         words.append(i)
#     elif(len(i.split()) == 2 and '(' not in i ):
#         words.append(i)
#     elif(len(i.split()) <= 3 and '(' not in i ):
#         words.append(i)
#     else:
#         words.append(i.split()[0])
# print(words)


headers = {
	"X-RapidAPI-Key": "477b42042fmsh1436202cccff4e6p113600jsn90a00cfda59b",
	"X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
}
def fetch_synonyms(word):

  url = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/synonyms"
  api_response = requests.request("GET", url, headers=headers)

  return json.loads(api_response.text)


syns=[]
words=['hi','inclusion']
for word in words:
    response = fetch_synonyms(word)
    if("synonyms" in response):
        syns.append(response["synonyms"])
    else:
        syns.append(word)

print(syns)





