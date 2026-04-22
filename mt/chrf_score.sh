#!/bin/bash

# conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nativebench

python chrf_score.py --predictions_file ./predictions.tsv