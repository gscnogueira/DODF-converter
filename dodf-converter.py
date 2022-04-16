#!/bin/python
import sys
import os.path
from os import path
import argparse
import pandas as pd
from tqdm import tqdm 
from utils.converter import gen_json
from utils.template import get_template

DESCRIPTION="Tool to convert data extracted from the Diário Oficial do Distrito Federal (DODF) by members of the KnEDLe project to the format supported by the data labeling tool Label Studio."
parser = argparse.ArgumentParser(description=DESCRIPTION,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 epilog='2022, Gabriel da Silva Corvino Nogueira (gab.nog94@gmail.com)')

parser.add_argument("--no-json", action="store_true", help="don't generate JSON file")
parser.add_argument("-t", "--template", action="store_true", help="generate template html files", default=False)
parser.add_argument("-d", "--output-dir", help="directory to store output", default='./')
parser.add_argument("file", help="path to dataset file")
args = parser.parse_args()
config = vars(args)
print(config)

df_file = config['file']
out_dir = config['output_dir']
df = pd.read_csv(df_file)
tipos_ato = df.dropna().tipo_rel.unique()

if not path.isdir(out_dir):
    raise ValueError("Output directory does not exist")
elif out_dir[-1] != '/':
    out_dir+='/'
    

print(f"Converting data from '{path}'...")
for tipo_ato in tqdm(tipos_ato):

    df_ato = df[df.tipo_rel ==  tipo_ato]
    
    if not config["no_json"]:
        json_content = gen_json(df_ato)
        json_file = open(out_dir + tipo_ato + '.json', 'w')
        json_file.write(json_content)
        json_file.close()

    if config["template"]:
        html_content = get_template(df_ato)
        html_file = open(out_dir + tipo_ato + '.html', 'w')
        html_file.write(html_content)
        html_file.close()

print(f"Done!")


    
