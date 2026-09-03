import re
import os
import argparse
from nltk.tokenize.punkt import PunktTokenizer
from gutenberg_cleaner import (simple_cleaner, 
                               super_cleaner)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('-n', '--name')
parser.add_argument('-l', '--lang')
arg = parser.parse_args()

if arg.lang == 'en':
    LANG = 'english'
    ABBR = {'mr','mrs','ms','dr','prof','st','rev'}
elif arg.lang == 'de':
    LANG = 'german'
    ABBR = {'hr','fr','dr','prof','st','hn'}

tokenizer = PunktTokenizer(LANG)
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

    # make special case for Kliphausen since it's not a Gutenberg proj text
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