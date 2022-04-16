#!/bin/python
import sys
import pandas as pd
from utils.converter import gen_json
from utils.template import get_template


path = sys.argv[1]
df = pd.read_csv(path)
tipos_ato = df.dropna().tipo_rel.unique()

print(tipos_ato)
for tipo_ato in tipos_ato:

    df_ato = df[df.tipo_rel ==  tipo_ato]
    json_content = gen_json(df_ato)
    json_file = open(tipo_ato + '.json', 'w')
    json_file.write(json_content)
    json_file.close()

    html_content = get_template(df_ato)
    html_file = open(tipo_ato + '.html', 'w')
    html_file.write(html_content)
    html_file.close()

    
