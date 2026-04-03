#!/bin/bash

# set environment variables
source ../set_keys.sh

# conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate nativebench

# prompt="Say the following sentence in Choctaw: 'Kʋta hosh chi pisʋt ayachi?'"
prompt="Say the following sentence in Muscogee: 'Vm estvlke Kaccvlke tos.'"

file_path='./mus08024-clip.wav'

# tts
# python speech_test.py "$prompt" tts --lang Choctaw --model deepseek-reasoner
# python speech_test.py "$prompt" tts --lang Choctaw --model claude-opus-4-6
# python speech_test.py "$prompt" tts --lang Choctaw --model gemini-2.5-pro-preview-tts
# python speech_test.py "$prompt" tts --lang Choctaw --model gpt-4o-mini-tts
# python speech_test.py "$prompt" tts --lang Choctaw --model gemini-2.5-flash-lite
# python speech_test.py "$prompt" tts --lang Choctaw --model gpt-5.2-2025-12-11
# python speech_test.py "$prompt" tts --lang Muscogee --model gpt-4o-mini-tts
# python speech_test.py "$prompt" tts --lang Muscogee --model gemini-2.5-pro-preview-tts
# python speech_test.py "$file_path" asr --lang Muscogee --model gemini-3.1-pro-preview
python speech_test.py "$file_path" asr --lang Muscogee --model gpt-4o-transcribe-diarize