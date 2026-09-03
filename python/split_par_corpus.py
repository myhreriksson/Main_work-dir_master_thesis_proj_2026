import json
import pandas as pd
import os
import argparse

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

de_path = os.path.join(arg.path, arg.inp_de)
en_path = os.path.join(arg.path, arg.inp_en)

eng_corpus = []
deu_corpus = []

# could defenitely have avoided making two redundant for-loops by writing smarter code, but I couldn't be bothered
for file in sorted(os.listdir(en_path)):
    with open(os.path.join(en_path, file), 'r', encoding='utf-8') as en:
        lines = en.readlines()
        for line in lines:
            eng_corpus.append(line.strip())

for file in sorted(os.listdir(de_path)):
    with open(os.path.join(de_path, file), 'r', encoding='utf-8') as de:
        lines = de.readlines()
        for line in lines:
            deu_corpus.append(line.strip())

with (
    open(os.path.join(arg.output + f'{arg.name}_train.json'), 'w', encoding='utf-8') as json_train,
    open(os.path.join(arg.output + f'{arg.name}_test.json'), 'w', encoding='utf-8') as json_test,
    open(os.path.join(arg.output + f'{arg.name}_dev.json'), 'w', encoding='utf-8') as json_dev
    ):
    pairs = []
    for en_line, de_line in zip(eng_corpus, deu_corpus):
        if len(en_line.split()) >= arg.min_len and len(de_line.split()) >= arg.min_len:
            pairs.append({'en': en_line, 'de': de_line})
    if arg.data_size != 'max':
        size = int(arg.data_size) * 1000
        df = pd.DataFrame(pairs).sample(n=size, random_state=21)
    else:
        df = pd.DataFrame(pairs).sample(frac=1, random_state=21)

    tot_rows = len(df) 
    train_rows = int(tot_rows * arg.split[0])
    test_rows = int(tot_rows * arg.split[1])

    train = df[:train_rows]
    test = df[train_rows:train_rows+test_rows]
    dev = df[train_rows+test_rows:]

    json_train.write(json.dumps(train.to_dict('records'), ensure_ascii=False, indent=2))
    json_test.write(json.dumps(test.to_dict('records'), ensure_ascii=False, indent=2))
    json_dev.write(json.dumps(dev.to_dict('records'), ensure_ascii=False, indent=2))