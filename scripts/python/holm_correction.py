import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--family')
parser.add_argument('-p', '--path')
arg = parser.parse_args()

balance = 'balanced', 'unbalanced'

def get_pvals(domain_path, family, *model):
    if family == 'inter':
        family_path = os.path.join(domain_path, f'comps_within_{model}')
    elif family == 'cross':
        family_path = os.path.join(domain_path, f'comps_across_models')
    for file in os.listdir(family_path):
        with open(file, 'r', encoding='utf-8') as f:
            return f.readlines()

bib_path = os.path.join(arg.path, 'bible')
get_pvals(bib_path, 'inter', 'bart')
get_pvals(bib_path, 'inter', 'nllb')

for b in balance:
    gam_path = os.path.join(arg.path, b)
    get_pvals(bib_path, 'cross')
