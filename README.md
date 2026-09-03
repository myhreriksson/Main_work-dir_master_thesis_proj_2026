### Venv Setup
INSTALL (mini/ana)CONDA \
conda create -n venv \
conda activate venv \
pip install accelerate datasets evaluate gutenberg_cleaner huggingface_hub matplotlib peft pypdf requests sacrebleu sentencepiece torch==2.6.0 trl unbabel-comet

python -<< EOF \
import nltk \
nltk.download('punkt_tab') \
EOF
___
### Model Setup
- Initial workspace setup; create directories.
- Retrieve models.

bash shell/init_setup.sh
___
### Preprocessing archaic data
- Retrieve archaic bible data and process it.
- Moves game_data to pseudo_deu and pseudo_eng.
- Moves bible_data to archaic_deu and archaic_eng.
- Retrieve archaic prose and poetry data, as well as process it.
- Manually process the prose data (use regex to remove footnotes, empty newlines, indentations, cursive markers).
- Regex for manual tokenization 1: (?<![.!?])\r?\n _replace with_ \s
- Regex for manual tokenization 2: ([.!?])\s+ _replace with_ $1\n
- The aforementioned does not produce a perfect tokenization, but adequate for the task.

bash run_preprocessing.sh
___
### Finetune NMT models
- Finetune model on specified data; *archaic* for tuning on bible data & *pseudo* for tuning on game data.

bash run_finetuning.sh
___
### Translate and evaluate
- Model inference: perform translations from English to German.
- Compute and store BLEU, TER, COMET scores in appropriate text files.
- Compute and store sacrebleu's and COMET's pairwise t-test bootstrapping p-values.

bash run_translations.sh
___
### Compute perplexity
- Compare the evaluation scores between baselines and tuned model translations.
- Use comparison to compute and store perplexity in appropriate text files.

bash run_autoregressive.sh