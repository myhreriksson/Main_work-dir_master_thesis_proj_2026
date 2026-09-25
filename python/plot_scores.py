import argparse
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path')
parser.add_argument('-s', '--style')
parser.add_argument('-o', '--output')
arg = parser.parse_args()

b = 'bleu'
c = 'comet'
t = 'ter'

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

def get_evals(dataset, metric):
    all_dat = {}
    for size, log in dataset.items():
        eval_steps = []
        eval_metric = []
        for entry in log:
            if 'eval_loss' in entry:
                eval_steps.append(entry['epoch'])
                eval_metric.append(entry[f'eval_{metric}'])
        all_dat[size] = eval_steps, eval_metric
    return all_dat

def get_plot(all_dat, axis, metric):
    for size, (eval_steps, eval_metric) in sorted(
        all_dat.items(), 
        key=lambda x: get_n(x[0].rstrip('k'))
        ):
        axis.plot(
            eval_steps,
            eval_metric,
            label=f'Validation {metric.upper()} for {size}',
            linewidth=2.5
        )

def get_axis(i, title, metric, xlabel):
    axes[i].set_title(title, fontsize=20)
    axes[i].set_xlabel(xlabel, fontsize=19)
    axes[i].set_ylabel(metric.upper(), fontsize=19)
    axes[i].grid(True)
    axes[i].tick_params(axis='both', labelsize=19)

bart_dataset = get_dataset('bart')
nllb_dataset = get_dataset('nllb')

all_bart_dat_b = get_evals(bart_dataset, b)
all_nllb_dat_b = get_evals(nllb_dataset, b)
all_bart_dat_c = get_evals(bart_dataset, c)
all_nllb_dat_c = get_evals(nllb_dataset, c)
all_bart_dat_t = get_evals(bart_dataset, t)
all_nllb_dat_t = get_evals(nllb_dataset, t)

fig, axes = plt.subplots(3, 2, figsize=(14, 18), sharey='row', sharex=True)
axes = axes.flatten()

bart_plot_0 = get_plot(all_bart_dat_b, axes[0], b)
bart_b_plot = get_axis(0, 'mBART-50', b, '')

nllb_plot_1 = get_plot(all_nllb_dat_b, axes[1], b)
nllb_b_plot = get_axis(1, 'NLLB-200', '', '')

bart_plot_2 = get_plot(all_bart_dat_c, axes[2], c)
bart_c_plot = get_axis(2, '', c, '')
axes[2].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
nllb_plot_3 = get_plot(all_nllb_dat_c, axes[3], c)
nllb_c_plot = get_axis(3, '', '', '')

bart_plot_4 = get_plot(all_bart_dat_t, axes[4], t)
bart_t_plot = get_axis(4, '', t, 'Epoch')

nllb_plot_5 = get_plot(all_nllb_dat_t, axes[5], t)
nllb_t_plot = get_axis(5, '', '', 'Epoch')

handles, _ = axes[0].get_legend_handles_labels()

fig.legend(
    handles, 
    ['Total', 'Cfig. 1', 'Cfig. 2', 'Cfig. 3', 'Cfig. 4', 'Cfig. 5'], 
    loc='lower center', 
    ncol=6,
    fontsize=19,
    frameon=False,
    bbox_to_anchor=(.5, -.004)
)

plt.tight_layout()
plt.subplots_adjust(bottom=.07)
plt.savefig(f'{arg.output}{arg.style}.png')
plt.show()