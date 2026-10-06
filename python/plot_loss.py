import argparse
import json
import os
import plot_scores as ps
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path')
parser.add_argument('-o', '--output')
arg = parser.parse_args()

domains = 'bible', 'balanced_bible', 'prose'

def get_dataset(model, lang):
    dataset = {}
    for domain in domains:
        path = os.path.join(arg.path, 'max', model, domain, f'trained_on_{lang}', 'training_log.json')
        with open(path, 'r', encoding='utf-8') as f:
            train_log = json.load(f)
            dataset[domain] = train_log
    return dataset

def get_evals(dataset):
    all_dat = {}
    for domain, log in dataset.items():
        train_steps = []
        train_loss = []
        eval_steps = []
        eval_loss = []
        for entry in log:
            if 'loss' in entry:
                train_steps.append(entry['epoch'])
                train_loss.append(entry[f'loss'])
            if 'eval_loss' in entry:
                eval_steps.append(entry['epoch'])
                eval_loss.append(entry[f'eval_loss'])
        all_dat[domain] = train_steps, train_loss, eval_steps, eval_loss
    return all_dat

colors = { # the RGB GUI is a pretty neat feature in VSCode
    't_bible': "#EE4848",
    'v_bible': "#F91900",
    't_balanced_bible': "#0060DD",
    'v_balanced_bible': "#0367E9",
    't_prose': "#00B418",
    'v_prose': "#05DA5A",
}

def get_plot(all_dat, axis):
    for domain, (train_steps, train_loss, eval_steps, eval_loss) in sorted(
        all_dat.items(), 
        key=lambda x: ps.get_n(x[0].rstrip('k'))
        ):
        axis.plot(
            train_steps,
            train_loss,
            color=colors[f't_{domain}'],
            label=f'Train LOSS for {domain}',
            linewidth=.5
        )
        axis.plot(
            eval_steps,
            eval_loss,
            color=colors[f'v_{domain}'],
            label=f'Val. LOSS for {domain}',
            linewidth=5
        )

eng_ds = get_dataset('qwen', 'eng')
deu_ds = get_dataset('qwen', 'deu')

all_dat_eng = get_evals(eng_ds)
all_dat_deu = get_evals(deu_ds)

fig, axes = plt.subplots(1, 2, figsize=(14, 8), sharey='row', sharex=True)
axes = axes.flatten()
ps.axes = axes

eng_plot = get_plot(all_dat_eng, axes[0])
qwen_eng_plot = ps.get_axis(0, 'Qwen3: English', 'loss', 'Epoch')

deu_plot = get_plot(all_dat_deu, axes[1])
qwen_deu_plot = ps.get_axis(1, 'Qwen3: German', '', 'Epoch')

handles, _ = axes[0].get_legend_handles_labels()
fig.legend(
    handles, 
    ['Train loss: Unbalanced', 'Validation loss: Unbalanced', 
     'Train loss: Balanced', 'Validation loss: Balanced',
     'Train loss: Prose', 'Validation loss: Prose'], 
    loc='lower center', 
    ncol=3,
    fontsize=19,
    frameon=False,
    bbox_to_anchor=(.5, -.004)
)

plt.tight_layout()
plt.subplots_adjust(bottom=.22)
plt.savefig(f'{arg.output}loss.png')
plt.show()