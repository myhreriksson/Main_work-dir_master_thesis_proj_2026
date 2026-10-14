import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--metric')
parser.add_argument('-b', '--baseline', type=int)
parser.add_argument('-d', '--degree')
parser.add_argument('-s', '--select', default=False)
arg = parser.parse_args()

csv_file = 'results/coefficients/lmm_data.csv'

cyan = '\033[96m'
reset = '\033[0m'

df = pd.read_csv(csv_file)
metric = df[arg.metric]

if arg.degree == 'high':
    filtered = df[metric > arg.baseline] # filters only high-scoring metrics
elif arg.degree == 'low':
    filtered = df[metric < arg.baseline] # filters only low-scoring metrics

counts = {
    'nllb': 0,
    'bart': 0,
    '3k': 0,
    '6k': 0,
    '9k': 0,
    '12k': 0,
    '15k': 0,
    'max': 0,
    'game': 0,
    'unbalanced_bible': 0,
    'balanced_bible': 0,
}

for _, row in filtered.iterrows():
    counts[row['model_design']] += 1
    counts[row['train_data_size']] += 1
    counts[row['train_domain']] += 1

if not arg.select:
    for k, v in counts.items():
        print(k,v)
else:
    print('Press \'Enter\' to cycle through sentences...')
    for _, row in filtered.iterrows():
        if len(row['sentence']) >= 5:
            input()
            print(
                f'Score: {cyan}{row[arg.metric]}{reset} | '
                f'Model design: {cyan}{row["model_design"]}{reset} | '
                f'Fine-tuning Config: {cyan}{row["train_data_size"]}{reset} | '
                f'Fine-tuning domain: {cyan}{row["train_domain"]}{reset}'
                f'\nSent: {row["sentence"]}'
            )