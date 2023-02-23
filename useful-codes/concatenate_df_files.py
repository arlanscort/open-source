'''
Arlan Scortegagna - jan/2023
Concatenate DataFrames contained in separated csv files into a single csv file which name is going to 'prefix'_concatenated.csv
'''

import argparse
import glob
import pandas as pd 

parser = argparse.ArgumentParser()
parser.add_argument('prefix', type=str, help = "Inform prefix of files")
args = parser.parse_args()

all_files = glob.glob(f'{args.prefix}*')
all_files = sorted(all_files)

print(f'Concatenando {all_files}')
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

df.to_csv(f'{args.prefix}_concatenated.csv', index=False)
