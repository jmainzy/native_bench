import torch
from transformers import pipeline

src_lang = "eng_Latn"
tgt_lang = "fra_Latn"
pipeline = pipeline(task="translation", model="facebook/nllb-200-distilled-600M", src_lang=src_lang, tgt_lang=tgt_lang, dtype=torch.float16, device=0)
pipeline("UN Chief says there is no military solution in Syria")