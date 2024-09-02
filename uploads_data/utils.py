# uploads_data/utils.py
import pandas as pd

def load_uploaded_file_to_dataframe(uploaded_file):
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path)  # Adjust according to your data structure
    return df
