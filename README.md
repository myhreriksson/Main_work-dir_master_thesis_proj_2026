# Seq2Seq translation of Dark Souls \& Elden Ring
In order for the following instructions to work, it is assumed that the instructions for the *Preprocessing_game-data_master_thesis_proj_2026* have been thoroughly followed.
___
### Initial Work directory setup
- Initial workspace setup; create directories.
- Retrieve models.
- Downloads and installs miniconda3.
```sh
bash shell/init_workdir.sh
```
Once the installation of miniconda3 is complete, retrieve the game data from the preprocessing_game-data repo:
```sh
mkdir tmp
git clone https://github.com/myhreriksson/Preprocessing_game-data_master_thesis_proj_2026 tmp/
mv tmp/game_data data
rm -fr tmp
```
___
### Venv Setup
```sh
conda create -n venv python==3.11 
conda activate venv 
pip install --upgrade pip 
pip install accelerate datasets evaluate gutenberg_cleaner huggingface_hub jsonlite matplotlib nltk optuna peft pypdf requests sacrebleu sentencepiece setuptools==80.9.0 torch==2.6.0 trl unbabel-comet==2.2.7
conda install -c conda-forge r-base r-lme4
```
```py
import nltk
nltk.download('punkt_tab')
```
___
### Preprocessing bible data + Retrieving FLORES 200
- Retrieves flores_200 data.
- Retrieves bible data and processes it.
- Moves game_data to game_deu and game_eng.
- Moves bible_data to bible_deu and bible_eng.
- Retrieve prose data, as well as process it.
- Manually process the prose data (use regex to remove footnotes, empty newlines, indentations, cursive markers).
- Regex for manual tokenization 1: (?<![.!?])\r?\n _replace with_ \s
- Regex for manual tokenization 2: ([.!?])\s+ _replace with_ $1\n
- The aforementioned does not produce a perfect tokenization, but adequate for the task.
```sh
bash run_preprocessing_pipeline.sh
```
___
### Finetune NMT models
- Finetune model on specified data; *bible* for tuning on bible data & *game* for tuning on game data.
```sh
bash run_finetuning_pipeline.sh
```
___
### Translate and evaluate
When translating non-fine-tuned baselines, the domain name refers to the *test* domain. \
In contrast, when translating using fine-tuned models, the domain name refers to the domain used during *training*.
- Model inference: perform translations from English to German.
- Compute and store BLEU, TER, COMET scores in appropriate text files.
- Compute and store sacrebleu's and COMET's pairwise t-test bootstrapping p-values.
```sh
bash run_translation_pipeline.sh
```
___
### Compute perplexity
- Compare the evaluation scores between baselines and tuned model translations.
- Use comparison to compute and store perplexity in appropriate text files.
```sh
bash run_perplexity_pipeline.sh
```
___
### Compute performance coefficients
- Compute statistical contribution of data size, model, and domain, to the predicted BLEU, COMET, and TER results.
```sh
bash run_coefficiency_pipeline.sh
```
___
### Optional commands
- Count word tokens:
- Plot evaluation scores:
- Cycle through archaic sentence pairs:
```sh
python python/count_toks.py [size] [domain] [min_word_count (4 or 5)]
bash shell/get_plot.sh [nmt] [domain] OR [llm]
bash shell/get_archaic_sents.sh [limit] [domain] + [config] [line] + [size] + [balance]
```