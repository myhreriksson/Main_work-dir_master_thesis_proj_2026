import argparse
from textwrap import dedent
import glob as g
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path')
parser.add_argument('-c', '--config')
parser.add_argument('-s', '--size')
parser.add_argument('-d', '--domain')
parser.add_argument('-l', '--line')
parser.add_argument('--limit')
arg = parser.parse_args()

# determiner mainly archaic pronouns in English
archaisms = {
    'thou','thee','ye','thy','thine','shalt','wilst','wouldst','would\'st',
    'yon','yonder','dost','hath','hast','beest','saith','bequeath','needest'
}

cyan = '\033[96m'
reset = '\033[00m'

en_path = g.glob(arg.path + r'_eng/*')[0]
de_path = g.glob(arg.path + r'_deu/*')[0]

if not arg.config:
    with (
        open(en_path, 'r', encoding='utf-8') as en,
        open(de_path, 'r', encoding='utf-8') as de
        ):
        e_lines = en.readlines()
        d_lines = de.readlines()
        candidates = []
        for idx, line in enumerate(e_lines):
            matches = 0
            for word in line.split():
                if word in archaisms:
                    matches += 1
            if matches == arg.limit and len(line.split()) <= 20:
                candidates.append((e_lines[idx], d_lines[idx], idx))
        remain = len(candidates)
        for pair in candidates:
            input(f'Press "{cyan}Enter{reset}" to continue.\n({remain} pair(s) remaining)\n')
            remain -= 1
            print(dedent(f'''\
            {pair[0]}\
            {pair[1]}\
            - Line: {pair[2]:,}
            '''))
        exit()

if arg.config == 'base':
    config = arg.config
elif arg.config == 'tuned':
    config = f'{arg.config}/{arg.size}'
path = fr'results/translations/{config}/{arg.domain}'
for file in sorted(os.listdir(path)):
    if not os.path.isdir(os.path.join(path, file)):
        fullpath = os.path.join(path, file)
        with (
            open(fullpath, 'r', encoding='utf-8') as f
            ):
            lines = f.readlines()
            print(dedent(f'''\
            {file}:
            {lines[int(arg.line)]}\
            '''))