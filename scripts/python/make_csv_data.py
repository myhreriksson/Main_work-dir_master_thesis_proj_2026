import csv
import os
import re

inp_path = 'files/'
out_path = 'results/coefficients/'

data = []
trans = []
bleu = []
comet = []
ter = []
evals = []

def get_lines(lst, file, *meta):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            lst.append((line.strip(), meta))

for file in sorted(os.listdir(inp_path)):
    
    if file.startswith('translation'):
        trans_file = os.path.join(inp_path, file)
        domain = file.split('-')[1] # includes balanced & unbalanced
        if domain.startswith('_'):
            domain = domain[1:]
        model = file.split('-')[2]
        size = re.split(r'[-.]', file)[3]
        get_lines(trans, trans_file, domain, model, size)

    elif file.startswith('sent_evals'):
        evals_file = os.path.join(inp_path, file)
        metric = re.split(r'[-.]', file)[-2]
        get_lines(globals()[metric], evals_file)
        if metric == 'comet':
            comet.pop()

assert len(trans) == len(bleu) == len(comet) == len(ter)

for b_line, c_line, t_line in zip(bleu, comet, ter):
    bleu_score = f'{float(b_line[0].split(" ")[2]):.1f}'
    comet_score = f'{float(c_line[0].split(" ")[-1]) * 100:.1f}'
    ter_score = f'{float(t_line[0].split(" ")[-1]):.1f}'
    evals.append((bleu_score, comet_score, ter_score))

for t, e in zip(trans, evals):
    dict = {
        'sentence': t[0],
        'train_domain': t[1][0],
        'model_design': t[1][1],
        'train_data_size': t[1][2],
        'bleu': e[0],
        'comet': e[1],
        'ter': e[2]
        }
    data.append(dict)

with open(f'{out_path}lmm_data.csv', 'w', newline='') as csv_file:
    fieldnames = ['sentence',
                  'train_data_size',
                  'model_design',
                  'train_domain',
                  'bleu',
                  'comet',
                  'ter']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)