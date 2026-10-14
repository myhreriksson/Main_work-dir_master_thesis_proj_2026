import json
import sys

def comet_extension(extension):
    if extension == 'txt':
        data = comet_file.read()
    elif extension == 'json':
        data = json.load(comet_file)
    return data

def get_significance(): # used in get_pvals.sh
    comet_data = comet_extension('json')
    sacre_data = json.load(sacre_file)
    # had to manually look and find the nesting in sacrebleu and comet
    comet = comet_data['statistical_results'][0]['paired_t-test']
    bleu = sacre_data[1]['BLEU']
    ter = sacre_data[1]['TER']
    # arbitrarily chose 15 decimal digits. will be fixed post holm correction later
    dict = {
        'BLEU p-value': f'{float(bleu["p_value"]):.10f}',
        'COMET p-value': f'{float(comet["p_value"]):.10f}',
        'TER p-value': f'{float(ter["p_value"]):.10f}'
    }
    with open(sys.argv[3], 'w') as f:
        json.dump(dict, f, indent=4)

def get_scores(): # used in get_evals.sh
    comet_data = comet_extension('txt')
    sacre_data = json.load(sacre_file)
    comet = float(comet_data.split()[-1]) * 100 # multiply by 100 for readability (optional)
    bleu = sacre_data[0]
    ter = sacre_data[1]
    ver_score = bleu['verbose_score']
    extra = ver_score.split('(')[1].split()
    with open(sys.argv[3], 'w', encoding='utf-8') as f:
        # the following formatting is for readability; chose to ignore unnecessary metadata
        f.write(
        f'''\
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
        Score: {float(comet) * 100} 
        ''')

if __name__=='__main__':
    with (
        open(sys.argv[1], 'r', encoding='utf-8') as sacre_file,
        open(sys.argv[2], 'r', encoding='utf-8') as comet_file
        ):
        if sys.argv[4] == 'score':
            get_scores()
        elif sys.argv[4] == 'significance':
            get_significance()