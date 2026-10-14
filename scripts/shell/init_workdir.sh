mkdir -p \
    models/base \
    models/tuned \
    scripts/python \
    scripts/shell \
    scripts/Rscript \
    results/evaluations \
    results/translations \
    data/_test-n-finetune_/bible_deu \
    data/_test-n-finetune_/bible_eng \
    data/_test-n-finetune_/game_deu \
    data/_test-n-finetune_/game_eng \
    data/bible_data \
    data/game_data \
    data/prose_data \

mv init_workdir.sh scripts/shell/

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh