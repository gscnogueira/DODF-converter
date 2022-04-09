import re
import pandas as pd
import json


ERROS = 0
def get_anotation(row, i):
    tab = 2*' '
    texto_rel = row.texto_rel
    texto_ent = row.texto_ent
    label = row.tipo_ent
    start = 0
    date_pattern = re.compile('^data_')
    is_date = (date_pattern.match(label) and len(texto_ent) < 3)
    try:
        if is_date:
            pattern = '\s' + texto_ent + '[\s|,|o]'
            start = re.search(pattern, texto_rel).start()
            start +=1
        else:
            start = texto_rel.index(texto_ent)
    except Exception as e:
        global ERROS 
        ERROS+=1
        print('-'*10 + 'ERRO ' + str(ERROS) + '-'*10)
        print("Erro:", e)
        print('id:', row.id_ato)
        print('texto_rel:',repr( texto_rel ))
        print('texto_ent:',repr( texto_ent ))
        print('label:',label)
    end = start + len(texto_ent)
    anotation = f"""
          {{
            "id": "{row.id_ato + '-' + str(i)}",
            "from_name": "label",
            "to_name": "text",
            "type": "labels",
            "value": {{
              "start": {start},
              "end": {end},
              "score": 1,
              "text": {json.dumps(texto_ent)},
              "labels": [
                "{label}"
              ]
            }}
          }}""" 
    return anotation

def gen_data(df):
    text = df.texto_rel.values[0]
    # print(text)
    result = [get_anotation(row,i) for i, row in df.iterrows()  if row.tipo_ent != row.tipo_rel ]
    result = ','.join(result)
    data = f'''
  {{
    "data": {{
      "text": {json.dumps(text)}
    }},
    "predictions": [
      {{
        "model_version": "Dados Anotados",
        "result": [{result}
        ]
      }}
    ]
  }} '''
    return data

def gen_json(df):
    beg = '['
    end = '\n]'

    ids = df.id_ato.unique()
    atos_agrupados = df.groupby('id_ato')
    atos_agrupados  = [atos_agrupados.get_group(id) for id in ids]
    data_block = [gen_data(ato) for ato in atos_agrupados ]
    data_block = ','.join(data_block)
    return (beg + data_block + end)



if __name__ == '__main__':

    df = pd.read_csv("../../dodf_atos_pessoal_final_version_fixed.csv")
    tipos_ato = df.tipo_rel.unique()
    atos = {}
    for tipo in tipos_ato:
        atos[tipo] = df[df.tipo_rel ==  tipo]

    df_ato = atos[tipos_ato[0]]
    json_content = gen_json(df_ato)
    json_file = open(tipos_ato[0] + '.json', 'w')
    json_file.write(json_content)
    json_file.close()
