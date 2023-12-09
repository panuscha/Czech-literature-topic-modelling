from bs4 import BeautifulSoup
import pandas as pd
import re


############ PATHS ##############

# picked dates 
date = "2010_2019"

# path to whole texts
b_path = "data/bel/{date}_beletrie.txt".format(date=date)
#b_path = "data/bel/{date}_no_names_beletrie.txt".format(date=date)

categories = "all"

# Out file with only lemmas
lemma_file = "data/lem/{date}_{categories}.txt".format(date=date, categories = categories)

# file with stop words
stopwords_file = "data/stop_words_czech.txt"


# names from texts
names_file = "data/bel/{date}_names.txt".format(date=date)

############# CODE #############

#  read names from name_file
def read_names(name_file):
    names_dict = {}
    with open(name_file, 'r', encoding="utf8") as f:
        for line in f.readlines():
            if "<doc" in line:
                pattern = r'title="(.*?)" author='
                # Find the substring using regex
                match = re.search(pattern, line)
                if match:
                    # Extract the substring
                    substring = match.group(1)
                    names_dict[substring] = []
            else:
                names_dict[substring].append(line.rstrip('\n'))
    return names_dict                

# open the file
with open(b_path, 'r', encoding="utf8") as f:
    data = f.read()

# xml
Bs_data = BeautifulSoup(data, "lxml")

# divide to books
s = Bs_data.find_all('doc')

count = 0    
names_dict = read_names(names_file)            

with open(lemma_file, "w", encoding="utf8") as f, open(stopwords_file, "r", encoding="utf8") as st: 
    stopwords = st.read()
    for inside in s:
        f.write("<doc title=\"" + inside['title'] + "\" author=\"" + inside['author'] + "\" publisher=\"" + inside['publisher'] +"\" first_published=\"" + inside['first_published'] + "\" authsex=\"" + inside['authsex'] + "\">\n")
        title = inside['title']
        split = inside.text.split('\n')
        for line in split:
                    s = line.split()
                    if len(s) > 2:
                        name = s[0]
                        word = s[2] 
                        category = s[5]
                        if categories == 'all': # 
                            if (name not in names_dict[title]) and (word not in names_dict[title]) and (word not in stopwords): #  and name not in names # ( category == "N"  or category == "A" )
                                count += 1 
                                f.write(word + ' ')
                        else: 
                            if (category == "N"  or category == "A" )  and  (name not in names_dict[title]) and (word not in names_dict[title]) and (word not in stopwords):
                                count += 1 
                                f.write(word + ' ')    

        f.write("\n</doc>\n")                
                       
print(count) 

