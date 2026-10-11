import json
import sys

def get_significance():
    alpha = 0.05
    txt_data = txt_file.read()
    json_data = json.load(json_file)
    comet = float(txt_data.split('p_value:')[1].split()[0])
    bleu = json_data[1]['BLEU']
    ter = json_data[1]['TER']

    if bleu['p_value'] < alpha:
        p_val_bleu = f'< {alpha}'
    else:
        p_val_bleu = f'> {alpha}'
    if ter['p_value'] < alpha:
        p_val_ter = f'< {alpha}'
    else:
        p_val_ter = f'> {alpha}'
    if comet < alpha:
        p_val_comet = f'< {alpha}'
    else:
        p_val_comet = f'> {alpha}'
    dict = {
        'BLEU p-value': f'{float(p_val_bleu):.10f}',
        'COMET p-value': f'{float(p_val_comet):.10f}',
        'TER p-value': f'{float(p_val_ter):.10f}'
    }
    with open(sys.argv[3], 'w') as json_file:
        json.dump(dict, json_file, indent=4)

def get_scores(): 
    txt_data = txt_file.read()
    json_data = json.load(json_file)
    comet = float(txt_data.split()[-1]) * 100
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

if __name__=='__main__':
    with (
        open(sys.argv[1]) as json_file,
        open(sys.argv[2], 'r', encoding='utf-8') as txt_file
        ):
        if sys.argv[4] == 'score':
            get_scores()
        elif sys.argv[4] == 'significance':
            get_significance()