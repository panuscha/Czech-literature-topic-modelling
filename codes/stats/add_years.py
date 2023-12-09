import pandas as pd

path = "../../data/topics/top2vec/books_info_topic_distance_"
df_years = pd.read_excel('birth_deaths.xlsx')

for years in ["1990_1999", "2000_2009", "2010_2019"]:
    df = pd.read_excel(path + "{y}.xlsx".format(y = years))

    born = [] 
    died = []
    for author in df.author:
        author = author+',' 
        try:
            r = df_years.loc[df_years['author'] == author,'year'].values[0]
            print(r)
            born.append(r[0:4])
            if len(r)>5:
                died.append(r[5:9])
            else:
                died.append('')    
        except:
            born.append('')
            died.append('')    
    df['born'] = born 
    df['died'] = died 
    df.to_excel(path+"born_died_{y}.xlsx".format(y=years))       
               