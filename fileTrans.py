import pandas as pd
from googletrans import Translator
import time
from tkinter import Tk, filedialog
import geopandas as gpd
from plyer import notification as plyer_notification  # Renamed to avoid conflict
import os

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def translate_text_with_retry(text, target_language):
    for _ in range(MAX_RETRIES):
        try:
            return translate_text(text, target_language)
        except AttributeError as e:
            print(f"Translation error: {e}. Retrying after {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    raise Exception(f"Failed after {MAX_RETRIES} retries.")

def print_and_save_translations(input_file, target_languages, text_column, output_excel_file, output_geojson_file):
    my_notification(title='Translation', message='Translation process started.')

    # Get the directory of the input file
    input_directory = os.path.dirname(input_file)

    if input_file.lower().endswith('.xlsx') or input_file.lower().endswith('.xls'):
        df = pd.read_excel(input_file)  # Read Excel file
        text_data = df[text_column].tolist()
    elif input_file.lower().endswith('.geojson'):
        gdf = gpd.read_file(input_file)  # Read GeoJSON file
        text_data = gdf[text_column].tolist()
    else:
        raise ValueError("Unsupported file format. Please provide an Excel (.xls/.xlsx) or GeoJSON (.geojson) file.")

    translations = {'Original_Text': text_data}

    for lang in target_languages:
        translated_column = f'Translation_{lang}'
        translations[translated_column] = []

    for text in text_data:
        for lang in target_languages:
            translated_text = translate_text_with_retry(text, lang)
            translations[f'Translation_{lang}'].append(translated_text)

    # Add translated columns to the existing DataFrame
    for lang in target_languages:
        df[f'Translation_{lang}'] = translations[f'Translation_{lang}']

    # Construct dynamic output file paths based on the input directory
    output_excel_file_path = os.path.join(input_directory, output_excel_file)
    output_geojson_file_path = os.path.join(input_directory, output_geojson_file)

    # Save the DataFrame with translated columns to the dynamic Excel file path
    with pd.ExcelWriter(output_excel_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Save translations to the dynamic GeoJSON file path
    if input_file.lower().endswith('.geojson'):
        output_gdf = gdf.copy()
        for lang in target_languages:
            output_gdf[f'Translation_{lang}'] = translations[f'Translation_{lang}']
        output_gdf.to_file(output_geojson_file_path, driver='GeoJSON')

    my_notification(title='Translation', message='Translation process completed.')

def select_file():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("Excel files", "*.xls;*.xlsx"), ("GeoJSON files", "*.geojson")]
    )
    return file_path

def my_notification(title, message):  # Changed function name
    plyer_notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification will disappear after 10 seconds
    )

if __name__ == "__main__":
    input_file_path = select_file()  # Allow the user to select an Excel or GeoJSON file
    # languages_to_translate = ['kn', 'bn', 'gu', 'ml', 'mr', 'or', 'pa', 'ta', 'te', 'ur']  # Language codes
    languages_to_translate = ['kn']  # Language codes
    text_column_to_translate = 'POI_NAME'  # Replace with the actual column name in your file
    output_excel_file_path = "Translated1.xlsx"  # Replace with the desired output Excel file name
    output_geojson_file_path = "output2.geojson"  # Replace with the desired output GeoJSON file name

    if input_file_path:
        print_and_save_translations(input_file_path, languages_to_translate, text_column_to_translate,
                                     output_excel_file_path, output_geojson_file_path)
