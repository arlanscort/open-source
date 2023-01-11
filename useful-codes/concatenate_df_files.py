'''
Created by Arlan Scortegagna, jan/2022
Concatenate several DataFrame, contained in separated files, into a single .csv
'''

import argparse
import glob
import pandas as pd 

parser = argparse.ArgumentParser()
parser.add_argument('prefix', type=str, help = "Inform prefix of files")
args = parser.parse_args()

all_files = glob.glob(f'{args.prefix}*')
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
df.to_csv(f'{args.prefix}_concatenated.csv')