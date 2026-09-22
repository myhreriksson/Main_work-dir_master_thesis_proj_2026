import argparse
import json
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path')
parser.add_argument('-s', '--style')
parser.add_argument('-o', '--output')
parser.add_argument('--metric')
arg = parser.parse_args()

def get_n(x):
    try:
        return int(x)
    except Exception:
        return 0

def get_dataset(model):
    dataset = {}
    for size in sorted(os.listdir(arg.path)):
        path = os.path.join(arg.path, size, model, arg.style, 'training_log.json')
        with open(path, 'r', encoding='utf-8') as f:
            log = json.load(f)
            dataset[size] = log
    return dataset

def get_evals(dataset):
    all_dat = {}
    for size, log in dataset.items():
        eval_steps = []
        eval_metric = []
        for entry in log:
            if 'eval_loss' in entry:
                eval_steps.append(entry['epoch'])
                eval_metric.append(entry[f'eval_{arg.metric}'])
        all_dat[size] = eval_steps, eval_metric
    return all_dat

def get_plot(all_dat, axis):
    for size, (eval_steps, eval_metric) in sorted(
        all_dat.items(), 
        key=lambda x: get_n(x[0].rstrip('k'))
        ):
        axis.plot(
            eval_steps,
            eval_metric,
            label=f'Validation {arg.metric.upper()} for {size}',
            linewidth=2.5
        )

bart_dataset = get_dataset('bart')
nllb_dataset = get_dataset('nllb')

all_bart_dat = get_evals(bart_dataset)
all_nllb_dat = get_evals(nllb_dataset)

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# bart subplot
bart_plot = get_plot(all_bart_dat, axes[0])
axes[0].set_title('BART', fontsize=16)
axes[0].set_xlabel('Epoch', fontsize=15)
axes[0].set_ylabel(arg.metric.upper(), fontsize=14)
axes[0].grid(True)
axes[0].tick_params(axis='both', labelsize=14)

# nllb subplot
nllb_plot = get_plot(all_nllb_dat, axes[1])
axes[1].set_title('NLLB', fontsize=16)
axes[1].set_xlabel('Epoch', fontsize=15)
axes[1].set_ylabel('')
axes[1].grid(True)
axes[1].tick_params(axis='both', labelsize=14)

handles, _ = axes[0].get_legend_handles_labels()

fig.legend(
    handles, 
    ['Total', 'Cfig. 1', 'Cfig. 2', 'Cfig. 3', 'Cfig. 4', 'Cfig. 5'], 
    loc='lower center', 
    ncol=6,
    fontsize=14,
    frameon=False,
    bbox_to_anchor=(.5, -.02)
)

plt.tight_layout()
plt.subplots_adjust(bottom=.15)
plt.savefig(f'{arg.output}{arg.style}_{arg.metric}.png')
plt.show()