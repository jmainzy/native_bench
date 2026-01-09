#!/bin/bash

# set environment variables
source ../set_keys.sh

# conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nativebench

# culture quiz
python culture_quiz.py --model gpt-4.1-2025-04-14