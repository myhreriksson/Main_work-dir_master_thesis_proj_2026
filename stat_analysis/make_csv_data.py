import csv
import os
import pandas as pd
import re

# bleu,comet,ter ~ data_size * model * domain + (1|sentence)

inp_path = 'stat_analysis/files'
out_path = 'stat_analysis'

data = []
trans = []
evals = []

def get_lines(lst, file, *meta):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            lst.append((line, meta))

def combine_evals(sacrebleu, comet): # vänta tills bleu & comet per sentence är färdiga.
    pass

for file in sorted(os.listdir(inp_path)):
    if file.startswith('translation'):
        trans_file = os.path.join(inp_path, file)
        domain = file.split('-')[1] # includes balanced & unbalanced
        model = file.split('-')[2]
        size = file.split('-')[3]
        get_lines(trans, trans_file, domain, model, size)

    elif file.startswith('sent_evals'):
        evals_file = os.path.join(inp_path, file) # vänta tills bleu & comet per sentence är färdiga.
        metric = re.split('-.', file)[-2]
        get_lines(evals, evals_file, metric)

for t, e in zip(trans, evals):
    dict = {
        'sentence': t[0],
        'domain': t[1],
        'model': t[2],
        'data_size': t[3],
        'bleu': e[0],
        'comet': e[1],
        'ter': e[2]
        }
    data.append(dict)

with open(f'{out_path}/data.csv', 'w', newline='') as csv_file:
    fieldnames = ['sentence','data_size','model','domain','bleu','comet','ter']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)