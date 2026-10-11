import argparse
from gutenberg_cleaner import (simple_cleaner, # absolute GOAT
                               super_cleaner)
from nltk.tokenize.punkt import PunktTokenizer
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('-n', '--name')
parser.add_argument('-l', '--lang')
arg = parser.parse_args()

if arg.lang == 'en':
    LANG = 'english'
    ABBR = {'mr','mrs','ms','dr','prof','st','rev'} # common eng abbreviations i found in data
elif arg.lang == 'de':
    LANG = 'german'
    ABBR = {'hr','fr','dr','prof','st','hn'} # common deu abbreviations i found in data

tokenizer = PunktTokenizer(LANG) # load tokenizer
tokenizer._params.abbrev_types.update(ABBR)

inp_path = os.path.join(arg.input, f'{arg.name}_raw.txt')
out_path = os.path.join(arg.output, f'{arg.lang.upper()}_{arg.name}_tokenized.txt')

with (
    open(inp_path, 'r', encoding='utf-8') as i_f,
    open(out_path, 'w', encoding='utf-8') as o_f
    ):
    txt = i_f.read()
    # make regex patterns
    pattern_1 = r'\[.*\]'
    pattern_2 = r'\s*\n\s*'
    pattern_3 = r'_+'

    # make special case for kliphausen since it's not a gutenberg proj text
    if re.search(r'.*Kliphausen.*', arg.name):
        # filter patterns
        txt = re.sub(pattern_1, '', txt)
        txt = re.sub(pattern_2, ' ', txt)
        txt = tokenizer.tokenize(txt)
        for sent in txt:
            o_f.write(sent + '\n')
    else:
        # apply gutenberg cleaners (absolutely based)
        txt = simple_cleaner(txt)
        txt = super_cleaner(txt)
        # filter patterns
        txt = re.sub(pattern_1, '', txt)
        txt = re.sub(pattern_2, ' ', txt)
        txt = re.sub(pattern_3, '', txt)
        txt = tokenizer.tokenize(txt)
        for sent in txt:
            o_f.write(sent + '\n')