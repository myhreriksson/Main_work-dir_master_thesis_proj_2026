import argparse
import heapq
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--metric')
parser.add_argument('-d', '--degree')
arg = parser.parse_args()

csv_file = 'results/coefficients/lmm_data.csv'

df = pd.read_csv(csv_file)
metric = df[arg.metric]

if arg.degree == 'good':
    sents = df.loc[metric > 90, 'sentence'].tolist()
    scores = df.loc[metric > 90, arg.metric].tolist()
elif arg.degree == 'bad':
    sents = df.loc[metric < 10, 'sentence'].tolist()
    scores = df.loc[metric < 10, arg.metric].tolist()

print(f'\nPress "ENTER" to cycle through sentences.')
for sent, score in zip(sents, scores):
    
    print(f'{score} | {sent}', end='', flush=True)