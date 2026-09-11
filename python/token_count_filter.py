import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--candidate')
parser.add_argument('-r', '--reference')
parser.add_argument('-o', '--output')
parser.add_argument('-l', '--lang')
arg = parser.parse_args()

if arg.lang == 'eng':
    LANG = 'EN'
elif arg.lang == 'deu':
    LANG = 'DE'

# balance bible according to game size, since game and prose are roughly same size
with (
    open(os.path.join(arg.candidate, f'bible_{LANG}.txt'), 'r', encoding='utf-8') as cand,
    open(os.path.join(arg.reference, f'game_{LANG}.txt'), 'r', encoding='utf-8') as ref, 
    open(os.path.join(arg.output, f'balanced_bible_{LANG}.txt'), 'w', encoding='utf-8') as out
    ):
    c_lines = cand.readlines()
    r_lines = ref.readlines()

    r_count = 0
    for r_line in r_lines:
        for tok in r_line.split():
            r_count += 1
    c_count = 0
    for c_line in c_lines:
        if c_count >= r_count:
            break
        out.write(c_line.strip() + '\n')
        for tok in c_line.split():
            c_count += 1
