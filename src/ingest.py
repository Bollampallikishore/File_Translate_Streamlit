import argostranslate.package
import argostranslate.translate
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import difflib
import pandas as pd
import csv

def translate_text(text, from_code, to_code):
    try:
        translated_text = argostranslate.translate.translate(text, from_code, to_code)
        return translated_text
    except Exception as e:
        return f"Translation Error: {str(e)}"

def translate_chunk(chunk, from_code, to_code, chunk_size=10000):
    translated_chunks = []
    for i in range(0, len(chunk), chunk_size):
        chunk_slice = chunk[i:i+chunk_size]
        with ThreadPoolExecutor(max_workers=4) as executor:
            translated_chunk = list(tqdm(executor.map(lambda x: translate_text(x, from_code, to_code), chunk_slice), total=len(chunk_slice), desc="Translating chunk", leave=False))
        translated_chunks.extend(translated_chunk)
    return pd.Series(translated_chunks)

def translate_dataframe(data, columns_to_translate, from_code, to_code):
    missing_columns = [col for col in columns_to_translate if col not in data.columns]
    if missing_columns:
        suggestions = {col: difflib.get_close_matches(col, data.columns, n=1) for col in missing_columns}
        suggestions_str = "; ".join([f"'{col}' not found. Did you mean '{sug[0]}'?" if sug else f"'{col}' not found and no similar column names detected." for col, sug in suggestions.items()])
        raise ValueError(suggestions_str)
    
    translated_data = data.copy()
    for column in columns_to_translate:
        translated_data[column] = translate_chunk(translated_data[column], from_code, to_code)
    return translated_data

def translate_ppt(presentation, slide_numbers, from_code, to_code):
    translated_presentation = presentation
    for slide_number in slide_numbers:
        slide = translated_presentation.slides[slide_number - 1]
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                shape.text = translate_text(shape.text, from_code, to_code)
    return translated_presentation

def translate_csv(data, columns_to_translate, from_code, to_code):
    reader = csv.DictReader(data.splitlines())
    fieldnames = reader.fieldnames
    
    missing_columns = [col for col in columns_to_translate if col not in fieldnames]
    if missing_columns:
        suggestions = {col: difflib.get_close_matches(col, fieldnames, n=1) for col in missing_columns}
        suggestions_str = "; ".join([f"'{col}' not found. Did you mean '{sug[0]}'?" if sug else f"'{col}' not found and no similar column names detected." for col, sug in suggestions.items()])
        raise ValueError(suggestions_str)
    
    translated_data = []
    for row in reader:
        for column in columns_to_translate:
            row[column] = translate_text(row[column], from_code, to_code)
        translated_data.append(row)
    return translated_data, fieldnames