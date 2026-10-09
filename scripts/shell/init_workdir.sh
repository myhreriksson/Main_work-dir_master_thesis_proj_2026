mkdir -p \
    models \
    models/base \
    models/tuned \
    scripts/python \
    scripts/shell \
    results/evaluations \
    results/translations \
    data/_test-n-finetune_/bible_deu \
    data/_test-n-finetune_/bible_eng \
    data/_test-n-finetune_/game_deu \
    data/_test-n-finetune_/game_eng \
    data/bible_data \
    data/game_data \
    data/prose_data \
    game_prep_repo \

mv init_workdir.sh scripts/shell

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh

hf download facebook/nllb-200-distilled-600M \
    --local-dir models/base/nllb

hf download facebook/mbart-large-50-many-to-many-mmt \
    --local-dir models/base/bart

hf download qwen/qwen3-0.6b \
    --local-dir models/base/qwen