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
# python vocab_quiz.py Choctaw --model gemini-3.1-pro-preview
# python vocab_quiz.py Muscogee --model gemini-3.1-pro-preview
# python vocab_quiz.py Choctaw --model deepseek-reasoner
# python vocab_quiz.py Choctaw --model claude-opus-4-6
# python vocab_quiz.py Mvskoke --model claude-opus-4-6
# python vocab_quiz.py Muscogee --model deepseek-chat
# python vocab_quiz.py Hawaiian --model claude-opus-4-6
# python vocab_quiz.py Hawaiian --model gemini-3.1-pro-preview
# python vocab_quiz.py Inuktitut --model claude-opus-4-6
# python vocab_quiz.py Cherokee --model gemini-3.1-pro-preview
# python vocab_quiz.py Cheyenne --model gemini-3.1-pro-preview
# python vocab_quiz.py Choctaw --model gpt-5.2-2025-12-11
# python vocab_quiz.py Cheyenne --model deepseek-reasoner
# python vocab_quiz.py Cherokee --model deepseek-reasoner
# python vocab_quiz.py Hawaiian --model deepseek-reasoner
# python vocab_quiz.py Choctaw --model gpt-4.1-2025-04-14
# python vocab_quiz.py Mvskoke --model gemini-3.1-pro-preview
# python vocab_quiz.py Choctaw --model gemini-3.1-pro-preview
# python vocab_quiz.py Hawaiian --model deepseek-reasoner
# python vocab_quiz.py Muscogee --model deepseek-chat
# python vocab_quiz.py Choctaw --model deepseek-chat
# python vocab_quiz.py Choctaw --model deepseek-reasoner
# python vocab_quiz.py Choctaw --model claude-opus-4-6
# python vocab_quiz.py Muscogee --model claude-opus-4-6
# python vocab_quiz.py Cheyenne --model claude-opus-4-6
# python vocab_quiz.py Cherokee --model claude-opus-4-6
# python vocab_quiz.py Hawaiian --model claude-opus-4-6
# python vocab_quiz.py Hawaiian --model gpt-5.2-2025-12-11
python vocab_quiz.py Cherokee --model deepseek-reasoner