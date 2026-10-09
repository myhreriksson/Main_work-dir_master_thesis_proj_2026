import json
import os
import sys

size = sys.argv[1]
domain = sys.argv[2]
min_sent = int(sys.argv[3])

path = f'data/_test-n-finetune_/_finetuning/{size}/'

sen_counter = 0
tok_counter = 0
tok_counter_en = 0
tok_counter_de = 0

for file in sorted(os.listdir(path)):
    if file.startswith(domain):
        with open(os.path.join(path,file), 'r', encoding='utf-8') as f:
            entries = json.load(f)
            for entry in entries:
                try:
                    if len(entry['en']) >= min_sent and len(entry['de']) >= min_sent:
                        sen_counter += 1
                        tok_counter_en += len(entry['en'].split())
                        tok_counter_de += len(entry['de'].split())
                except KeyError:
                    if len(entry['text']) >= min_sent:
                        sen_counter += 1
                        tok_counter += len(entry['text'].split())

avg_sent = tok_counter / sen_counter
avg_de_sent = tok_counter_de / sen_counter
avg_en_sent = tok_counter_en / sen_counter

if domain != 'prose':
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