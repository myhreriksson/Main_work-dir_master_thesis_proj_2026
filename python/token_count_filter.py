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

if arg.domain == 'pseudo':
    key = 'de'
    cand_name = f'archaic_{arg.split}.json'
    ref_name = f'{arg.domain}_{arg.split}.json'
    out_name = f'balanced_archaic_{arg.split}.json'
elif arg.domain == 'prose':
    key = 'text'
    cand_name = f'{arg.lang}_archaic_{arg.split}.json'
    ref_name = f'{arg.lang}_{arg.domain}_{arg.split}.json'
    out_name = f'balanced_{arg.lang}_archaic_{arg.split}.json'

with (
    open(os.path.join(arg.path, cand_name), 'r', encoding='utf-8') as cand,
    open(os.path.join(arg.path, ref_name), 'r', encoding='utf-8') as ref, 
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