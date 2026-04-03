#!/bin/bash

# set environment variables
source ../set_keys.sh

# conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nativebench

# vocabulary quiz
# python mt_quiz.py --phrase_list_file ./phrase_list.tsv
# python mt_quiz.py --phrase_list_file ./phrase_list.tsv --model gemini-3.1-pro-preview
# python mt_quiz.py --phrase_list_file ./phrase_list.tsv --model deepseek-reasoner
# python mt_quiz.py --phrase_list_file ./phrase_list.tsv --model claude-opus-4-6
# python mt_quiz.py --phrase_list_file ./hawaiian_list.tsv --model claude-opus-4-6
# python mt_quiz.py --phrase_list_file ./hawaiian_list.tsv --model gemini-3.1-pro-preview
# python mt_quiz.py --phrase_list_file ./phrase_list.tsv --model gpt-5.2-2025-12-11
# python mt_quiz.py --phrase_list_file ./phrase_list.tsv --model deepseek-reasoner
# python mt_quiz.py --phrase_list_file ./phrase_list.tsv --model claude-opus-4-6
# python mt_quiz.py --phrase_list_file ./phrase_list.tsv --model gemini-3.1-pro-preview
python mt_quiz.py --phrase_list_file ./phrase_list.tsv --model gpt-4.1-2025-04-14
python mt_quiz.py --phrase_list_file ./mus-chw-list.tsv --model gpt-5.2-2025-12-11