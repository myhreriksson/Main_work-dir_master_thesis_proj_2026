import json
import os
import sys

#1 = size
#2 = domain
#3 = min(count(sent))

path = f'data/_test-n-finetune_/_finetuning/{sys.argv[1]}/'
min_len = int(sys.argv[3])

sen_counter = 0
tok_counter = 0
tok_counter_en = 0
tok_counter_de = 0

for file in sorted(os.listdir(path)):
    if file.startswith(sys.argv[2]):
        with open(os.path.join(path,file), 'r', encoding='utf-8') as f:
            entries = json.load(f)
            for entry in entries:
                try:
                    if len(entry['en']) >= min_len and len(entry['de']) >= min_len:
                        sen_counter += 1
                        tok_counter_en += len(entry['en'].split())
                        tok_counter_de += len(entry['de'].split())
                except KeyError:
                    if len(entry['text']) >= min_len:
                        sen_counter += 1
                        tok_counter += len(entry['text'].split())

avg_sent = tok_counter / sen_counter
avg_de_sent = tok_counter_de / sen_counter
avg_en_sent = tok_counter_en / sen_counter

if min_len == 4:
    print(f'''\
    Aligned sentences: {sen_counter:,}
    Avg. sent. deu length: {avg_de_sent:.2f}
    Avg. sent. eng length: {avg_en_sent:.2f}
    German word tokens: {tok_counter_de:,}
    English word tokens: {tok_counter_en:,}\
    ''')
elif min_len == 5:
    print(f'''\
    Sentences: {sen_counter:,}
    Avg. sent. length: {avg_sent:.2f}
    Word tokens: {tok_counter:,}\
    ''')