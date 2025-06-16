#!/usr/bin/env python3
import os
import sys
import shutil
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

# --- CONFIGURATION ---
PDF_DIR = "/Users/niklascanova/Desktop/PDF"
OUT_DIR = "/Users/niklascanova/Desktop/PDF_text"
# ----------------------

# Ensure output folder exists
os.makedirs(OUT_DIR, exist_ok=True)

# Auto-discover tesseract
tesseract_path = shutil.which("tesseract")
if not tesseract_path:
    sys.exit(
        "ERROR: Tesseract OCR not found. "
        "Install it with Homebrew (`brew install tesseract`) "
        "or ensure it's on your PATH."
    )
pytesseract.pytesseract.tesseract_cmd = tesseract_path

for fname in sorted(os.listdir(PDF_DIR)):
    if not fname.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_DIR, fname)
    reader   = PdfReader(pdf_path)
    full_txt = []

    print(f"Processing {fname} …")

    for i, page in enumerate(reader.pages, start=1):
        # 1) Try native text
        page_text = page.extract_text() or ""
        if page_text.strip():
            full_txt.append(page_text)
        else:
            # 2) Fallback to OCR
            images = convert_from_path(pdf_path, first_page=i, last_page=i)
            for img in images:
                ocr_txt = pytesseract.image_to_string(img)
                full_txt.append(ocr_txt)

    # Write out combined text
    base, _ = os.path.splitext(fname)
    out_path = os.path.join(OUT_DIR, base + ".txt")
    with open(out_path, "w", encoding="utf-8") as out_f:
        out_f.write("\n\n".join(full_txt))

    print(f" → saved text to {out_path}")

print("All done!")
