import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inp_path')
parser.add_argument('-o', '--out_path')
parser.add_argument('-l', '--lang')
parser.add_argument('-d', '--domain')
arg = parser.parse_args()

domain = []

if arg.lang == 'eng':
    lang_prefix = 'EN'
elif arg.lang == 'deu':
    lang_prefix = 'DE'

for file in os.listdir(arg.inp_path):
    if arg.domain == 'prose':
        # this is a TERRIBLE solution; absolute fucking trash,
        # but I realized WAAY too late I have to adapt to different file sizes (I should be banned from writing code again)
        if re.search(r'.*Kliphausen.*', file):
            limit = 59000
        elif re.search(r'.*Grimmelshausen.*', file):
            limit = 59000
        elif re.search(r'.*Reuter.*', file):
            limit = 32000
        elif re.search(r'.*Bunyan.*', file):
            limit = 55000
        elif re.search(r'.*Lodge.*', file):
            limit = 40000
        elif re.search(r'.*Sidney.*', file):
            limit = 55000
        if file.startswith(lang_prefix):
            with open(os.path.join(arg.inp_path, file), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                selected = []
                word_count = 0
                for line in lines[100:]:
                    words = line.split()
                    selected.append(line)
                    word_count += len(words)
                    if word_count >= int(limit):
                        break
                domain.extend(selected)

with open(os.path.join(arg.out_path, f'{arg.domain}_{lang_prefix}.txt'), 'w', encoding='utf-8') as f:
    for sent in domain:
        f.write(sent)
    