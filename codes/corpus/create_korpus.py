import re 

'''
Selects fiction books from corpus SYNv9 and divides it into three categories based on source language
'''

path = "D:\\syn_v9-2"

read = "N"

b1_path = '../../data/bel/1990_1999_beletrie.txt'
b2_path = '../../data/bel/2000_2009_beletrie.txt'
b3_path = '../../data/bel/2010_2019_beletrie.txt'

with open(path, encoding="utf8") as f, open (b1_path , 'w', encoding="utf8") as b1, open (b2_path , 'w', encoding="utf8") as b2, open (b3_path , 'w', encoding="utf8") as b3:
    for line in f:
        if "FIC: beletrie"in line and "NOV: próza" in line and "srclang=\"cs: čeština" in line and "GEN: obecné publikum" in line:
            first_published = int(re.search('(?<=first_published=").{4}', line).group(0))
            if first_published > 1989 and first_published < 2000:
                print(line)
                read = "B1"
                b1.write(line)
            elif first_published > 1999 and first_published < 2010: 
                print(line)
                read = "B2" 
                b2.write(line) 
            elif first_published > 2009 and first_published < 2020: 
                print(line)
                read = "B3"
                b3.write(line)
            else:
                read = "N"
        elif "srclang=" in line:
            read = "N"  
        elif  read == "B1":
            b1.write(line)
        elif  read == "B2":
            b2.write(line)  
        elif  read == "B3":
            b3.write(line)     