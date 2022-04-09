import pandas as pd

def get_template(df):
    labels = df.tipo_ent.unique()
    beg_template = '<View>\n  <Labels name="label" toName="text">'
    end_template = '  </Labels>\n  <Text name="text" value="$text"></Text>\n</View>'
    labels = [' '*4 + f'<Label value="{label}"></Label>' for label in labels]
    labels = '\n'.join(labels)
     
    template = '\n'.join(( beg_template, labels, end_template ))
    return template

