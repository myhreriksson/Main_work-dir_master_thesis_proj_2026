import argparse
import json
import os
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('-d', '--domain')
parser.add_argument('-l', '--lang')
parser.add_argument('-s', '--split', nargs=3, type=float)
parser.add_argument('--min_len', type=int, default=3)
arg = parser.parse_args()

'''
this script is specifically for prose data, as it uses different keys
than the par_corpus script. this script uses "text" for all lines.
'''

path = os.path.join(arg.input, arg.domain + f'_{arg.lang}')

corpus = [] # accumulate all text from prose data here

for file in sorted(os.listdir(path)):
    with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if len(line.split()) >= arg.min_len:
                corpus.append(line.strip())

with (
    open(os.path.join(arg.output, f'{arg.lang}_{arg.domain}_train.json'), 'w', encoding='utf-8') as json_train,
    open(os.path.join(arg.output, f'{arg.lang}_{arg.domain}_test.json'), 'w', encoding='utf-8') as json_test,
    open(os.path.join(arg.output, f'{arg.lang}_{arg.domain}_dev.json'), 'w', encoding='utf-8') as json_dev
    ):
    entries = [{'text': line} for line in corpus] # list of dict entries
    df = pd.DataFrame(entries).sample(frac=1, random_state=21) # chose 21 for reproducibility

    tot_rows = len(df)
    train_rows = int(tot_rows * arg.split[0])
    test_rows = int(tot_rows * arg.split[1])

    train = df[:train_rows] # selects first row up till 80% of rows
    test = df[train_rows:train_rows+test_rows] # starts from 80% and continues for another 10%
    dev = df[train_rows+test_rows:] # starts from 90% and selects the remainder

    json_train.write(json.dumps(train.to_dict('records'), ensure_ascii=False, indent=2))
    json_test.write(json.dumps(test.to_dict('records'), ensure_ascii=False, indent=2))
    json_dev.write(json.dumps(dev.to_dict('records'), ensure_ascii=False, indent=2))