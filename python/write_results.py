import sys
import json

# NOTE: these functions are purely for aesthetic reasons; nicer to read results!

def get_significance():
    alpha = 0.05
    txt_data = txt_file.read()
    json_data = json.load(json_file)
    comet = float(txt_data.split('p_value:')[1].split()[0])
    bleu = json_data[1]['BLEU']
    ter = json_data[1]['TER']

    if bleu['p_value'] < alpha:
        p_val_bleu = f'< alpha={alpha}'
    else:
        p_val_bleu = ''
    if ter['p_value'] < alpha:
        p_val_ter = f'< alpha={alpha}'
    else:
        p_val_ter = ''
    if comet < alpha:
        p_val_comet = f'< alpha={alpha}'
    else:
        p_val_comet = ''
    with open(sys.argv[3], 'w', encoding='utf-8') as f:
        f.write(f'''\
        Statistical significance for pairwise t-test bootstrapping for {sys.argv[1].split('/')[2]}
        
        Metric: BLEU
        p-value: {bleu['p_value']:.4f} {p_val_bleu}

        Metric: TER
        p-value: {ter['p_value']:.4f} {p_val_ter}

        Metric: COMET
        p-value: {comet} {p_val_comet}
        ''')

def get_scores(): 
    txt_data = txt_file.read()
    json_data = json.load(json_file)
    comet = txt_data.split()[-1]
    bleu = json_data[0]
    ter = json_data[1]
    ver_score = bleu['verbose_score']
    extra = ver_score.split('(')[1].split()
    with open(sys.argv[3], 'w', encoding='utf-8') as f:
        f.write(f'''\
        Evaluation scores for {sys.argv[1].split('/')[2]}
    
        Metric: BLEU
        Score: {bleu['score']}
        - Verbose Scores
            - Unigram: {ver_score.split('/')[0]}
            - Bigram: {ver_score.split('/')[1]}
            - Trigram: {ver_score.split('/')[2]}
            - Quadragram: {ver_score.split('/')[3].split('(')[0]}
                
            - Hypothesis length: {extra[8]}
            - Reference length: {extra[11][:-1]}
            - Ratio: {extra[5]}
            - Brevity penalty: {extra[2]}
        - Number of References: {bleu['nrefs']}
        - Capitalization: {bleu['case']}
    
        Metric: TER
        Score: {ter['score']}
        - Number of References: {ter['nrefs']}
        - Capitalization: {ter['case']}
        - Normalization: {ter['norm']}
        - Punctuation: {ter['punct']}
    
        Metric: COMET
        Score: {comet}
        ''')

with (
    open(sys.argv[1]) as json_file,
    open(sys.argv[2], 'r', encoding='utf-8') as txt_file
    ):
    if sys.argv[4] == 'score':
        get_scores()
    elif sys.argv[4] == 'bootstrap':
        get_significance()