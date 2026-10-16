import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--degree')
parser.add_argument('-m', '--metric')
arg = parser.parse_args()

csv_file = 'results/coefficients/lmm_data.csv'

cyan = '\033[96m'
reset = '\033[0m'

df = pd.read_csv(csv_file).sample(frac=1)
metric = df[arg.metric]

if arg.degree == 'high':
    filtered = df[metric > np.percentile(metric, 95)] # contains the uppermost percentile
elif arg.degree == 'low':
    filtered = df[metric < np.percentile(metric, 5)] # contains the lowermost percentile

print('Press \'Enter\' to cycle through sentences...')
count = 0
for _, row in filtered.iterrows():
    if len(row['sentence'].split()) >= 5:
        if count > 2:
            break
        input()
        print(
            f'Score: {cyan}{row[arg.metric]}{reset} | '
            f'Model design: {cyan}{row["model_design"]}{reset} | '
            f'Fine-tuning Config: {cyan}{row["train_data_size"]}{reset} | '
            f'Fine-tuning domain: {cyan}{row["train_domain"]}{reset}'
            f'\nSent: {row["sentence"]}'
        )
        count += 1