import pandas as pd

def get_template(df):
    labels = df.tipo_ent.unique()
    beg_template = '<View>\n  <Labels name="label" toName="text">'
    end_template = '  </Labels>\n  <Text name="text" value="$text"></Text>\n</View>'
    labels = [' '*4 + f'<Label value="{label}"></Label>' for label in labels]
    labels = '\n'.join(labels)
     
    template = '\n'.join(( beg_template, labels, end_template ))
    return template





if __name__ == "__main__":

    df = pd.read_csv("../../dodf_atos_pessoal_final_version.csv")
    tipos_ato = df.tipo_rel.unique()
    for tipo in tipos_ato:
        print('-'*10 + tipo + '-'*10)
        df_sub = df[df.tipo_rel ==  tipo]
        print(get_template(df_sub))





