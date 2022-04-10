#!/bin/python
import sys
import pandas as pd
from utils.converter import gen_json
from utils.template import get_template


df = pd.read_csv("../dodf_atos_pessoal_final_version_fixed.csv")

tipos_ato = df.tipo_rel.unique()

atos = {}

for tipo in tipos_ato:
    atos[tipo] = df[df.tipo_rel ==  tipo]
    
ato = int( sys.argv[1] )
df_ato = atos[tipos_ato[ato]]
tipo_ato = tipos_ato[ato]

json_content = gen_json(df_ato)
json_file = open(tipo_ato + '.json', 'w')
json_file.write(json_content)
json_file.close()

html_content = get_template(df_ato)
html_file = open(tipo_ato + '.html', 'w')
html_file.write(html_content)
html_file.close()
