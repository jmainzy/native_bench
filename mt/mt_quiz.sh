#!/bin/bash

# set environment variables
source ../set_keys.sh

# conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nativebench

# vocabulary quiz
python mt_quiz.py --phrase_list_file ./phrase_list_demo.tsv
