import pandas as pd
from pymarc import map_xml
path = "aut_ja.xml.gz"
birth_death = {}

def do_it(r):
    for line in r.get_fields('100'):
        try:
            name = line['a'] 
            if name in birth_death.keys():
                years = line['d']
                if years[0:4] >  birth_death[name][0:4]: 
                    birth_death[name] = years 
            else:
                birth_death[name] = line['d']
        except:
            continue

map_xml(do_it, path)

df = pd.DataFrame(birth_death, index=[0]).T.to_excel('birth_deaths.xlsx')
