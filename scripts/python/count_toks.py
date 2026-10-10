import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--size')
parser.add_argument('-d', '--domain')
parser.add_argument('-b', '--balance', type=bool)
parser.add_argument('--min_sent_len', type=int)
arg = parser.parse_args()

path = f'data/_test-n-finetune_/_finetuning/{arg.size}/'

sen_counter = 0
tok_counter = 0
tok_counter_en = 0
tok_counter_de = 0

if arg.balance:
    domain = f'balanced_{arg.domain}'
else:
    domain = arg.domain

for file in sorted(os.listdir(path)):
    if file.startswith(domain):
        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            entries = json.load(f)
            for entry in entries:
                try:
                    if len(entry['en'].split()) >= arg.min_sent_len and len(entry['de'].split()) >= arg.min_sent_len:
                        sen_counter += 1
                        tok_counter_en += len(entry['en'].split())
                        tok_counter_de += len(entry['de'].split())
                except KeyError:
                    if len(entry['text'].split()) >= arg.min_sent_len:
                        sen_counter += 1
                        tok_counter += len(entry['text'].split())

avg_sent = tok_counter / sen_counter
avg_de_sent = tok_counter_de / sen_counter
avg_en_sent = tok_counter_en / sen_counter

if arg.domain != 'deu_prose' and arg.domain != 'eng_prose':
    print(f'''\
    Aligned sentences: {sen_counter:,}
    Avg. sent. deu length: {avg_de_sent:.2f}
    Avg. sent. eng length: {avg_en_sent:.2f}
    German word tokens: {tok_counter_de:,}
    English word tokens: {tok_counter_en:,}\
    ''')
else:
    print(f'''\
    Sentences: {sen_counter:,}
    Avg. sent. length: {avg_sent:.2f}
    Word tokens: {tok_counter:,}\
    ''')