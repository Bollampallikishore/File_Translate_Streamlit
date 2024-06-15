# File Language Translator Application

## Overview

This application is a web-based tool built with Streamlit to translate text in various file formats including Excel (XLSX), PowerPoint (PPTX), and CSV. It leverages the Argos Translate library to perform translations between specified languages. The tool supports batch translation of text in selected columns or slides, ensuring an efficient workflow for users needing to translate large amounts of content

## Features

- __Excel File Translation__: Translate text in selected columns of an Excel file.
- __PowerPoint File Translation__: Translate text in specified slides of a PowerPoint presentation.
- __CSV File Translation__: Translate text in selected columns of a CSV file.
- __Multithreading Support__: Uses multithreading to speed up the translation process.
- __Error Handling__: Provides suggestions for correcting column names in case of typos or missing columns.

## Installation

### Prerequisites
- Python 3.7 or higher
- Streamlit
- Pandas
- Argos Translate
- TQDM
- Python-PPTX

## Steps
1. Clone the repository
```
git clone https__://github.com/yourusername/file-translator.git

```
2. Install the required packages

```
pip install -r requirements.txt
```
```
cd src
```
3. Run the application

```
streamlit run main.py
```
## usage
### Uploading Files

1. __Upload your file__: 
- Select the file you want to translate (Excel, PPTX, or CSV).
2. __Select Columns/Slides__:
- For Excel and CSV files, choose the columns to translate.
- For PPTX files, specify the slide numbers to translate.
3. __Translate__:
- Click the "Translate" button to initiate the translation.
4. __Download__:
- Once the translation is complete, download the translated file.

## Supported File 

- __Excel (XLSX)__: Upload an Excel file, select the columns for translation, and download the translated file.
- __PowerPoint (PPTX)__: Upload a PowerPoint file, specify the slides for translation, and download the translated presentation.
- __CSV__: Upload a CSV file, select the columns for translation, and download the translated CSV.

## Translation Configuration

- __Language Codes__: The application is configured to translate from German (de) to English (en). This can be modified in the code to support other language pairs available in Argos Translate.

## Streamlit Interface

- __File Upload__: Allows users to upload files.
- __Column/Slide Selection__: Provides a UI to select columns or slides to translate.
- __Translation and Download__: Executes the translation and provides a download button for the translated file.