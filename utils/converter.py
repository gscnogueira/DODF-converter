import re
import pandas as pd
import json

ERROS = 0

def get_anotation(row):
    tab = 2*' '
    texto_rel = row.texto_rel
    texto_ent = row.texto_ent
    label = row.tipo_ent
    start = 0
    danger_classes = [re.compile('^data_'),
                      re.compile('^classe'),
                      re.compile('^padrao'),
                      ]


    danger = [bool(danger_class.match(label)) for danger_class in danger_classes]
    is_dangerous = (any(danger) and len(texto_ent) < 3)

    pagina_dodf = re.compile('^pagina_dodf')
    numero_dodf = re.compile('^numero_dodf')
    
    is_pagina = pagina_dodf.match(label)
    is_numero = numero_dodf.match(label)

    try:
        if is_dangerous:
            pattern = '\s' + texto_ent + '[,|o]?\s'
            start = re.search(pattern, texto_rel).start()
            start +=1
        elif is_pagina:
            pattern = '([pP]a(\-\s)?g(\-\s)?i(\-\s)?n(\-\s)?a(\-\s)?s?)|(pa?g\.?)|(p\.)'
            start = re.search(pattern, texto_rel).start()
            start = texto_rel.index(texto_ent, start)
        elif is_numero:
            pattern = '(DO[\s]?DF)|(Edicao Extra)|(Diario Oficial)'
            start = re.search(pattern, texto_rel).end()
            start = texto_rel.index(texto_ent, start)
        else:
            start = texto_rel.index(texto_ent)
    except Exception as e:
        global ERROS
        ERROS+=1
        print('-'*10 + 'ERRO' + '-'*10)
        print(f'Erro n°{ERROS}')
        print("Descrição:", e)
        print(f'id:{row.id_ato}')
        print('label:',label,end=2*'\n')
        print('texto_rel:',repr( texto_rel ), end=2*'\n')
        print('texto_ent:',repr( texto_ent ), end=2*'\n')
        it()
    end = start + len(texto_ent)
    anotation = f"""
          {{
            "from_name": "label",
            "to_name": "text",
            "type": "labels",
            "value": {{
              "start": {start},
              "end": {end},
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
    result = [get_anotation(row) for _, row in df.iterrows()  if row.tipo_ent != row.tipo_rel ]
    result = ','.join(result)
    data = f'''
  {{
    "data": {{
      "text": {json.dumps(text)}
    }},
    "annotations": [
      {{
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
