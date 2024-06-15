import pandas as pd
import streamlit as st
import argostranslate.package
import argostranslate.translate
import io
from pptx import Presentation
import csv


from ingest import translate_dataframe, translate_ppt, translate_csv


def main():
    st.title("File Translator")

    uploaded_file = st.file_uploader("Upload your file (Excel, PPTX, CSV)", type=["xlsx", "pptx", "csv"])
    if uploaded_file is not None:
        from_code = "de"
        to_code = "en"
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code,
                available_packages
            )
        )
        installed_package = argostranslate.package.install_from_path(package_to_install.download())

        file_type = uploaded_file.name.split('.')[-1]

        if file_type == "xlsx":
            data = pd.read_excel(uploaded_file)
            st.write("Uploaded Excel file:")
            st.write(data.head())

            columns_to_translate = st.multiselect("Select the columns to translate:", data.columns)

            if st.button("Translate Excel"):
                try:
                    translated_data = translate_dataframe(data, columns_to_translate, from_code, to_code)
                    st.write("Translated data:")
                    st.write(translated_data.head())

                    output = io.BytesIO()
                    translated_data.to_excel(output, index=False)
                    output.seek(0)

                    translated_filename = f"{uploaded_file.name.split('.xlsx')[0]}_translated.xlsx"
                    st.download_button(
                        label="Download Translated Excel File",
                        data=output,
                        file_name=translated_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except ValueError as e:
                    st.error(str(e))

        elif file_type == "pptx":
            presentation = Presentation(uploaded_file)
            slide_numbers_input = st.text_input("Enter the slide numbers to translate (comma-separated):", "1")
            slide_numbers = [int(num.strip()) for num in slide_numbers_input.split(",")]

            if st.button("Translate PPTX"):
                translated_presentation = translate_ppt(presentation, slide_numbers, from_code, to_code)
                
                output = io.BytesIO()
                translated_presentation.save(output)
                output.seek(0)

                translated_filename = f"{uploaded_file.name.split('.pptx')[0]}_translated.pptx"
                st.download_button(
                    label="Download Translated PPTX File",
                        data=output,
                        file_name=translated_filename,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )

        elif file_type == "csv":
            data = uploaded_file.read().decode("utf-8")
            reader = csv.DictReader(data.splitlines())
            st.write("Uploaded CSV file columns:")
            st.write(reader.fieldnames)

            columns_to_translate = st.multiselect("Select the columns to translate:", reader.fieldnames)

            if st.button("Translate CSV"):
                try:
                    translated_data, fieldnames = translate_csv(data, columns_to_translate, from_code, to_code)

                    output = io.StringIO()
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(translated_data)
                    output.seek(0)

                    translated_filename = f"{uploaded_file.name.split('.csv')[0]}_translated.csv"
                    st.download_button(
                        label="Download Translated CSV File",
                        data=output.getvalue(),
                        file_name=translated_filename,
                        mime="text/csv"
                    )
                except ValueError as e:
                    st.error(str(e))

if __name__ == "__main__":
    main()