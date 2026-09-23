import pandas as pd
import numpy as np

def prepare_mapped_data(file_path, mapping):
    # Wczytanie pliku
    try:
        df = pd.read_csv(file_path)
        if len(df.columns) == 1:
            df = pd.read_csv(file_path, sep=';')
    except Exception:
        df = pd.read_csv(file_path, sep=';')

    df.columns = df.columns.str.strip()

    date_col = str(mapping.get('date_col', '')).strip()
    value_col = str(mapping.get('value_col', '')).strip()
    category_col = str(mapping.get('category_col', '')).strip()

    if date_col not in df.columns or value_col not in df.columns:
        return {"error": "Error: Couldn't find columns in the file."}

    df['sys_date'] = df[date_col]
    df['sys_value'] = df[value_col]

    columns_to_keep = ['sys_date', 'sys_value']
    if category_col and category_col in df.columns:
        df['sys_category'] = df[category_col]
        columns_to_keep.append('sys_category')

    df = df[columns_to_keep].copy()
    initial_count = len(df)

    if initial_count == 0:
        return {"error": "Error: File do not contain any data."}

    df['sys_date'] = pd.to_datetime(df['sys_date'], errors='coerce')
    
    valid_dates_count = df['sys_date'].notna().sum()
    
    if valid_dates_count < (initial_count * 0.3):
        return {"error": "Critical Error: Cannot parse dates. You likely mapped the Revenue column to the Date field."}
        
    if (df['sys_date'].dt.year == 1970).mean() > 0.5:
        return {"error": "Critical Error: Invalid dates detected. You mapped a numeric field to the Date field."}

    df = df.dropna(subset=['sys_date'])

    if df['sys_value'].dtype == 'object':
        df['sys_value'] = df['sys_value'].astype(str).str.replace(r'[^\d,-]', '', regex=True)
        df['sys_value'] = df['sys_value'].str.replace(',', '.')

    df['sys_value'] = pd.to_numeric(df['sys_value'], errors='coerce')
    
    valid_values_count = df['sys_value'].notna().sum()
    
    if valid_values_count < (len(df) * 0.3):
        return {"error": "Critical Error: Cannot parse revenue values. You likely mapped the Date column to the Revenue field."}

    df = df.dropna(subset=['sys_value'])

    return df