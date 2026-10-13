import argparse
import json
import os
from statsmodels.stats.multitest import multipletests

# define args
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--family')
parser.add_argument('-i', '--inp_path')
parser.add_argument('-o', '--out_path')
arg = parser.parse_args()

'''
this script has A LOT of comments, because it got very confusing and overly
convoluted as scripting progressed. please bear this in mind: it might be 
unnecessarily complicated...
'''

balance = 'balanced', 'unbalanced' # list of domain balance options

def get_pvals(domain_path, family, *model):
    '''
    retrieves every raw p-value from the input path and stores them
    family-wise. cross-model p-values in one list, inter-model p-values
    in another list.
    '''
    domain = domain_path.split('/')
    if domain[-1] != 'bible':
        domain = f'{domain[-2]} {domain[-1]}'
    else:
        domain = domain[-1]
    '''
    above is just for domain names, below is start of function.
    '''
    lst = []
    if family == 'inter':
        family_path = os.path.join(domain_path, f'comps_within_{model[0]}')
    elif family == 'cross':
        family_path = os.path.join(domain_path, f'comps_across_models')
    for file in sorted(os.listdir(family_path)):
        with open(os.path.join(family_path, file), 'r', encoding='utf-8') as json_file:
            if family == 'cross':
                dict = {f'{domain.upper()} {file}': json.load(json_file)}
            elif family == 'inter':
                dict = {f'{model[0].upper()} {domain.upper()} {file}': json.load(json_file)}
            lst.append(dict)
    return lst

def get_raw(family):
    '''
    loop through the family list; each family contains three domains 
    (bible, unbalanced_game, balanced_game). For every file across all domains,
    get the values to the BLEU, COMET, and TER keys (see line 57). save a reference 
    of the file for later (see line 58); will be used when overwriting the 
    uncorrected p-values. make values into floats and return for correction.
    '''
    refs = [] # list of references
    p_vals = []
    for domain in family:
        for file in domain:
            if arg.family == 'cross':
                key_val = next(iter(file.values())) # get dict of key:value pairs
                refs.append(key_val) # save a reference of the key:value pairs
                p_vals.extend([ # extend list of values to empty list
                    float(key_val.get('BLEU p-value')),
                    float(key_val.get('COMET p-value')),
                    float(key_val.get('TER p-value'))
                ])
            elif arg.family == 'inter':
                for nest in file: # added an extra loop for inter-model comps
                    key_val = next(iter(nest.values())) # get dict of key:value pairs
                    refs.append(key_val) # save a reference of the key:value pairs
                    p_vals.extend([ # extend list of values to empty list
                        float(key_val.get('BLEU p-value')),
                        float(key_val.get('COMET p-value')),
                        float(key_val.get('TER p-value'))
                    ])
    return refs, p_vals

cross_pvals = [] # all pvals for the cross-model family 
inter_pvals = [] # all pvals  for the inter-model family

bib_path = os.path.join(arg.inp_path, 'bible') # path for all bible pvals
bib_cross = get_pvals(bib_path, 'cross') # get bible pvals from cross-model comps
bib_inter = (get_pvals(bib_path, 'inter', 'bart'), # get bible pvals from inter-model (bart) comps
             get_pvals(bib_path, 'inter', 'nllb')) # get bible pvals from inter-model (nllb) comps
cross_pvals.append(bib_cross) # append list of bible pvals from cross-model comps 
inter_pvals.append(bib_inter) # append tuple of lists of bible pvals from inter-model comps (both bart and nllb)
for b in balance: # loop over balanced and unbalanced subdirs
    gam_path = os.path.join(arg.inp_path, 'game', b) # path for all game pvals
    gam_cross = get_pvals(gam_path, 'cross') # get game pvals from cross-model comps
    gam_inter = (get_pvals(gam_path, 'inter', 'bart'), # get game pvals from inter-model (bart) comps
                 get_pvals(gam_path, 'inter', 'nllb')) # get game pvals from inter-model (nllb) comps
    cross_pvals.append(gam_cross) # append list of game pvals from cross-model comps
    inter_pvals.append(gam_inter) # append tuple of lists of game pvals from inter-model comps (both bart and nllb)


family_values = globals()[f'{arg.family}_pvals'] # pretty funny name
keys = 'BLEU p-value', 'COMET p-value', 'TER p-value'
refs, p_vals = get_raw(family_values)
corrected = multipletests(p_vals, method='holm')[1] # takes list; returns list

corrs = iter(corrected) # make list iterable
for key_val_pair in refs:
    for key in keys:
        key_val_pair[key] = f'{next(iter(corrs)):.8f}' # replace old raw vals with corrected; iterate through list!

with open(os.path.join(arg.out_path ,f'{arg.family}-model_pvals.json'), 'w', encoding='utf-8') as f:
    json.dump(family_values, f, indent=2)