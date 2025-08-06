import fitz  # PyMuPDF
import json
import os

def pdf_to_json(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    json_data = {}

    for i, page in enumerate(doc):
        page_number = f"page_{i + 1}"
        json_data[page_number] = page.get_text()

    doc.close()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"Saved: {output_path}")

def convert_all_pdfs_in_folder(pdf_folder):
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            json_name = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(".", json_name)  # Save in current directory
            pdf_to_json(pdf_path, output_path)

# === Set your PDF folder here ===
pdf_folder = r"C:\Users\jlpal\OneDrive\Desktop\cleantime_app_desktop\PDF_files"

convert_all_pdfs_in_folder(pdf_folder)
