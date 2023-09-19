# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_language_detection.ipynb.

# %% auto 0
__all__ = ['language_codes', 'download_lang_model', 'load_model', 'detect_language']

# %% ../nbs/01_language_detection.ipynb 3
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# %% ../nbs/01_language_detection.ipynb 5
def download_lang_model(model_path: str, model_name: str):
    """Download a Hugging Face language detection model and tokenizer 
    to the specified directory"""

    # Check if the directory already exists
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Save the model and tokenizer to the specified directory
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)

# %% ../nbs/01_language_detection.ipynb 8
language_codes = [
    'ja',
    'nl',
    'ar',
    'pl',
    'de',
    'it',
    'pt',
    'tr',
    'es',
    'hi',
    'el',
    'ur',
    'bg',
    'en',
    'fr',
    'zh',
    'ru',
    'th',
    'sw',
    'vi'
]

# %% ../nbs/01_language_detection.ipynb 10
def load_model(model_path: str):
    """Load a Hugging Face model and tokenizer from the specified directory"""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return model, tokenizer

# %% ../nbs/01_language_detection.ipynb 12
def detect_language(text: str, model, tokenizer):
    """Detect the language of a given text"""

    # Truncate the text to 512 characters
    text = text[:512]

    # Tokenize the text
    inputs = tokenizer(text, return_tensors="pt")

    # Get the prediction
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(-1)
    
    return(language_codes[int(predictions)])