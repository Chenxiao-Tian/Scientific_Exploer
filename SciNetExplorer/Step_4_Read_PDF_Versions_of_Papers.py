# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 20:46:11 2024

@author: ct347
"""

import PyPDF2
import yake
import spacy
from spacy.matcher import Matcher
import os
import threading
import pdfplumber  # Added this line

def read_pdf(pdf_file_path):
    """Extracts text from a PDF file."""
    text = ''
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ''
    except Exception as e:
        print(f"Error reading PDF file at {pdf_file_path}: {e}")
    return text

def extract_text_sections(pdf_path):
    """Extracts text sections from a PDF file."""
    text = read_pdf(pdf_path)
    references_text = ""
    annexes_text = ""
    body_text = ""

    if text:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    if 'References' in page_text or 'Bibliography' in page_text:
                        references_text += page_text + "\n"
                    elif 'Annex' in page_text or 'Appendix' in page_text:
                        annexes_text += page_text + "\n"
                    else:
                        body_text += page_text + "\n"

    return references_text, annexes_text, body_text

def process_pdf_and_write_to_text(pdf_file_path, output_dir):
    """Processes the PDF and writes results to a text file."""
    output_file_path = os.path.join(output_dir, os.path.basename(pdf_file_path) + ".txt")
    references_text, annexes_text, body_text = extract_text_sections(pdf_file_path)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("References:\n")
        file.write(references_text + "\n")
        file.write("Annexes/Appendices:\n")
        file.write(annexes_text + "\n")
        file.write("Body Text:\n")
        file.write(body_text + "\n")

def process_bib_file(bib_file_path, output_dir):
    """Process a BibTeX file containing article entries."""
    with open(bib_file_path, 'r', encoding='utf-8') as bibfile:
        bib_data = bibfile.read()
        entries = bib_data.split('\n\n')

        def process_entries(entries):
            for entry in entries:
                if entry.strip() == '':
                    continue
                article_data = {}
                lines = entry.split('\n')
                for line in lines:
                    if line.strip() == '':
                        continue
                    key_value = line.split('=', 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        key = key.strip().lower()
                        value = value.strip().strip('{').strip('},')
                        article_data[key] = value

                pdf_path = article_data.get('file', '')
                if pdf_path and pdf_path.endswith('.pdf'):
                    process_pdf_and_write_to_text(pdf_path, output_dir)

        # Split entries into chunks for parallel processing
        chunk_size = len(entries) // 4
        chunks = [entries[i:i+chunk_size] for i in range(0, len(entries), chunk_size)]

        # Create threads for processing chunks
        threads = []
        for chunk in chunks:
            thread = threading.Thread(target=process_entries, args=(chunk,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

# Example usage
def main_output_4(bib_file_path,output_dir):
    bib_file_path = '2024-CEE520.bib'
    output_dir = 'Step_4_Output'
    os.makedirs(output_dir, exist_ok=True)
    
    process_bib_file(bib_file_path, output_dir)

if __name__ == "__main__":
    bib_file_path = '2024-CEE520.bib'
    output_dir = 'Step_4_Output'
    main_output_4(bib_file_path,output_dir)
