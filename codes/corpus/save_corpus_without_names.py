from bs4 import BeautifulSoup
import pandas as pd
import requests

date = '1990_1999'
b_path = "data/bel/{date}_beletrie.txt".format(date=date)

with open(b_path, 'r', encoding="utf8") as f:
    data = f.read()

Bs_data = BeautifulSoup(data, "lxml")

s = Bs_data.find_all('doc')

no_names_file = "data/bel/{date}_no_names_beletrie.txt".format(date=date)
stopwords_file = "data/stop_words_czech.txt"

count = 0    
parameters = {'data' : 'data',
              'input': 'vertical',
              'output': 'vertical'} 

names_file = "data/bel/{date}_names.txt".format(date=date)

with open(no_names_file, "w", encoding="utf8") as f, open(stopwords_file, "r", encoding="utf8") as st, open(names_file, "w", encoding="utf8") as n: 
    stopwords = st.read()
    for inside in s:
        f.write("<doc title=\"" + inside['title'] + "\" author=\"" + inside['author'] + "\" publisher=\"" + inside['publisher'] +"\" first_published=\"" + inside['first_published'] + "\" authsex=\"" + inside['authsex'] + "\">\n")
        n.write("<doc title=\"" + inside['title'] + "\" author=\"" + inside['author'] + "\" publisher=\"" + inside['publisher'] +"\" first_published=\"" + inside['first_published'] + "\" authsex=\"" + inside['authsex'] + "\">\n")
        names = []

        for text in inside.find_all('block'):
            parameters['data'] = text.text
            try:
                response = requests.get(url = "http://lindat.mff.cuni.cz/services/nametag/api/recognize", params=parameters)
                result = response.json()['result'] 
                s = result.split()  
                if len(s) > 1 and (s[1] == 'pf' or s[1] == 'ps') and not(s[2] in names) :
                    names.append(s[2])
                    n.write(s[2] + "\n")
                    print("name: " + s[2]) 
            # start = end
            except:
                print("Text: \n" + text.text)
            split = text.text.split('\n')
            for line in split:  
                s = line.split()
                if len(s) > 2:
                    name = s[0]
                    word = s[2] 
                    category = s[5]
                    if name not in names :
                        count += 1 
                        f.write(line + '\n')       
        f.write("\n</doc>\n")      