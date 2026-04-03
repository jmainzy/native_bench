#!/bin/bash

# set environment variables
source ../set_keys.sh

# conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nativebench

# prompt="Tell me the story about Rabbit Steals Fire. Tell it in Muscogee, in the style of a Muscogee traditional story."
prompt="Tell me the story about Why the Possum Has a Hairless Tail. Tell it in Choctaw, in the style of a Choctaw traditional story. Also provide English translation."

# prompt

# python story_test.py "$prompt" --lang Muscogee --model deepseek-reasoner
# python story_test.py "$prompt" --lang Muscogee --model claude-opus-4-6
# python story_test.py "$prompt" --lang Muscogee --model gemini-3.1-pro-preview
# python story_test.py "$prompt" --lang Muscogee --model gpt-5.2-2025-12-11


# python story_test.py "$prompt" --lang Choctaw --model deepseek-reasoner
python story_test.py "$prompt" --lang Choctaw --model claude-opus-4-6
python story_test.py "$prompt" --lang Choctaw --model gemini-3.1-pro-preview
python story_test.py "$prompt" --lang Choctaw --model gpt-5.2-2025-12-11