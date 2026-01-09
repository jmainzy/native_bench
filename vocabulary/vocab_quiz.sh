#!/bin/bash

# set environment variables
source ../set_keys.sh

# conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nativebench

# vocabulary quiz
# python vocab_quiz.py Muscogee --model gpt-4.1-2025-04-14
# python vocab_quiz.py Choctaw --model gpt-4.1-2025-04-14
# python vocab_quiz.py Muscogee --model gpt-5.2-2025-12-11
# python vocab_quiz.py Muscogee --model gemini-2.5-flash-lite
python vocab_quiz.py Muscogee