# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 20:31:02 2024

@author: ct347
"""

import PyPDF2
import yake
import spacy
from spacy.matcher import Matcher
import os
import threading

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

def extract_keywords(text):
    """Extracts keywords from text using YAKE."""
    kw_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=10, features=None)
    keywords = kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

def analyze_text(text):
    """Analyzes text to extract methodologies and research outcomes using spaCy."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Define patterns for methodology and results
    methodology_patterns = [[{"LEMMA": {"IN": ["method", "approach", "technique", "algorithm"]}}]]
    results_patterns = [[{"LEMMA": {"IN": ["result", "outcome", "finding", "conclusion", "data"]}}]]

    matcher = Matcher(nlp.vocab)
    matcher.add("Methodology", methodology_patterns)
    matcher.add("Results", results_patterns)

    methodologies = []
    results = []

    for _, start, end in matcher(doc):
        span = doc[start:end].sent
        if "Methodology" in nlp.vocab.strings:
            methodologies.append(span.text)
        if "Results" in nlp.vocab.strings:
            results.append(span.text)

    main_topics = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]
    return methodologies, results, main_topics

def truncate_text(text, max_length=900):
    """Truncates text to a specified maximum length."""
    return text[:max_length]

def process_pdf_and_write_to_text(pdf_file_path, output_dir):
    """Processes the PDF and writes results to a text file."""
    output_file_path = os.path.join(output_dir, os.path.basename(pdf_file_path) + ".txt")
    text = read_pdf(pdf_file_path)
    if not text:
        print(f"No text extracted from PDF: {pdf_file_path}")
        return

    keywords = extract_keywords(text)
    methodologies, outcomes, main_topics = analyze_text(text)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("Extracted Keywords:\n")
        file.write(truncate_text(", ".join(keywords)) + "\n\n")
        file.write("Main Topics:\n")
        file.write(truncate_text(", ".join(main_topics)) + "\n\n")
        file.write("Methodologies:\n")
        file.write(truncate_text(" ".join(methodologies)) + "\n\n")
        file.write("Research Outcomes:\n")
        file.write(truncate_text(" ".join(outcomes)) + "\n")

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
def main_output_5(bib_file_path,output_dir):
    os.makedirs(output_dir, exist_ok=True)
    process_bib_file(bib_file_path, output_dir)
# Example usage
if __name__ == "__main__":
    bib_file_path = '2024-CEE520.bib'
    output_dir = 'step_5_Output' 
    main_output_5(bib_file_path, output_dir)
