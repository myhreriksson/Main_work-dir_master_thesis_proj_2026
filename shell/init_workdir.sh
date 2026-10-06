mkdir -p \
    models \
    models/base \
    models/tuned \
    python \
    shell \
    results/evaluations \
    results/translations \
    data/_test-n-finetune_/bible_deu \
    data/_test-n-finetune_/bible_eng \
    data/_test-n-finetune_/game_deu \
    data/_test-n-finetune_/game_eng \
    data/bible_data \
    data/game_data \
    data/prose_data \

mv init_setup.sh shell

hf download facebook/nllb-200-distilled-600M \
    --local-dir models/base/nllb

hf download facebook/mbart-large-50-many-to-many-mmt \
    --local-dir models/base/bart

hf download qwen/qwen3-0.6b \
    --local-dir models/base/qwen