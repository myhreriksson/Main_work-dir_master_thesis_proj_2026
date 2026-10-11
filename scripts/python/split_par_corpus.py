import argparse
import json
import os
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path')
parser.add_argument('-d', '--inp_de')
parser.add_argument('-e', '--inp_en')
parser.add_argument('-o', '--output')
parser.add_argument('-n', '--name')
parser.add_argument('-s', '--split', nargs=3, type=float)
parser.add_argument('--data_size')
parser.add_argument('--min_len', type=int, default=1)
arg = parser.parse_args()

'''
this script is specifically for bible- and video game data, as it 
uses english and german prefix as dict keys when writing to json.
'''

de_path = os.path.join(arg.path, arg.inp_de)
en_path = os.path.join(arg.path, arg.inp_en)

def get_lines(path, corpus):
    for file in sorted(os.listdir(path)):
        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                corpus.append(line.strip())

eng_corpus = []
deu_corpus = []
get_lines(en_path, eng_corpus)
get_lines(de_path, deu_corpus)

with (
    open(os.path.join(arg.output + f'{arg.name}_train.json'), 'w', encoding='utf-8') as json_train,
    open(os.path.join(arg.output + f'{arg.name}_test.json'), 'w', encoding='utf-8') as json_test,
    open(os.path.join(arg.output + f'{arg.name}_dev.json'), 'w', encoding='utf-8') as json_dev
    ):
    pairs = []
    for en_line, de_line in zip(eng_corpus, deu_corpus):
        # ignores english and german lines with very short sent length (like grunts and laughter)
        if len(en_line.split()) >= arg.min_len and len(de_line.split()) >= arg.min_len:
            pairs.append({'en': en_line, 'de': de_line})
    if arg.data_size != 'max':
        size = int(arg.data_size[:-1]) * 1000
        size = min(size, len(pairs))
        df = pd.DataFrame(pairs).sample(n=size, random_state=21) # chose 21 for reproducibility
    else:
        df = pd.DataFrame(pairs).sample(frac=1, random_state=21) # chose 21 for reproducibility

    tot_rows = len(df) 
    train_rows = int(tot_rows * arg.split[0])
    test_rows = int(tot_rows * arg.split[1])

    train = df[:train_rows] # selects first row up till 80% of rows
    test = df[train_rows:train_rows+test_rows] # starts from 80% and continues for another 10%
    dev = df[train_rows+test_rows:] # starts from 90% and selects the remainder

    json_train.write(json.dumps(train.to_dict('records'), ensure_ascii=False, indent=2))
    json_test.write(json.dumps(test.to_dict('records'), ensure_ascii=False, indent=2))
    json_dev.write(json.dumps(dev.to_dict('records'), ensure_ascii=False, indent=2))