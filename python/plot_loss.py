import argparse
import json
import os
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path')
parser.add_argument('-m', '--model')
parser.add_argument('-s', '--style')
parser.add_argument('-o', '--output')
parser.add_argument('--metric')
arg = parser.parse_args()

dataset = {}

for size in sorted(os.listdir(arg.path)):
    path = os.path.join(arg.path, size, arg.model, arg.style, 'training_log.json')
    with open(path, 'r', encoding='utf-8') as f:
        log = json.load(f)
        dataset[size] = log

all_dat = {}

def get_n(x):
    try:
        return int(x)
    except Exception:
        return 0

for size, log in dataset.items():
    eval_steps = []
    eval_metric = []
    for entry in log:
        if 'eval_loss' in entry:
            eval_steps.append(entry['epoch'])
            eval_metric.append(entry[f'eval_{arg.metric}'])
    all_dat[size] = eval_steps, eval_metric

plt.figure(figsize=(10,8))
for size, (eval_steps, eval_metric) in sorted(all_dat.items(), 
                                              key=lambda x: get_n(x[0].rstrip('k'))
                                              ):
    plt.plot(eval_steps, eval_metric, label=f'Validation {arg.metric.upper()} for {size}')

plt.xlabel('Epoch')
plt.ylabel(f'{arg.metric.upper()}')
plt.legend()
plt.savefig(f'{arg.output}loss_{arg.model}_{arg.style}_{arg.metric}.png')
plt.show()