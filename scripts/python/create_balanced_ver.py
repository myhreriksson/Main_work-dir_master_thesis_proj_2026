import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path')
parser.add_argument('-c', '--candidate')
parser.add_argument('-r', '--reference')
parser.add_argument('-o', '--output')
parser.add_argument('-s', '--split')
parser.add_argument('-d', '--domain')
parser.add_argument('-l', '--lang')
arg = parser.parse_args()

'''
this script mainly balances total number of word tokens per fine-tuning config size
in the bible data. this way, another version of the bible dataset is created, which,
for each config size, has approximately the same number of word tokens as prose and
video game data has. this dataset is referred to as balanced_bible. NOTE!
if some file or dir is called "balanced_game" or "unbalanced_game", it means 
video game text was translated using a model fine-tuned on balanced/unbalanced bible
data. not anything else.
'''

if arg.domain == 'game':
    key = 'de'
    cand_name = f'bible_{arg.split}.json'
    ref_name = f'{arg.domain}_{arg.split}.json'
    out_name = f'balanced_bible_{arg.split}.json'
elif arg.domain == 'prose':
    key = 'text'
    cand_name = f'{arg.lang}_bible_{arg.split}.json'
    ref_name = f'{arg.lang}_{arg.domain}_{arg.split}.json'
    out_name = f'balanced_{arg.lang}_bible_{arg.split}.json'

with (
    open(os.path.join(arg.path, cand_name), 'r', encoding='utf-8') as cand, # not to be confused with translation cand
    open(os.path.join(arg.path, ref_name), 'r', encoding='utf-8') as ref, # not to be confused with translation ref
    open(os.path.join(arg.output, out_name), 'w', encoding='utf-8') as out 
    ):
    c_count = 0
    r_count = 0
    selected = []

    r_entries = json.load(ref)
    for r_entry in r_entries:
        for r_tok in r_entry[key].split():
            r_count += 1

    c_entries = json.load(cand)
    for c_entry in c_entries:
        selected.append(c_entry)
        if c_count >= r_count:
            break
        for c_tok in c_entry[key].split():
            c_count += 1

    json.dump(selected, out, ensure_ascii=False, indent=2)