# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 19:29:09 2024

@author: ct347
"""

import bibtexparser

def extract_meta_information(bibtex_file, output_file):
    """
    Function to extract metadata from a BibTeX file and write it to an output file.
    
    Parameters:
    bibtex_file (str): The path to the BibTeX file containing bibliographic entries.
    output_file (str): The path to the file where extracted metadata will be saved.
    """
    
    # Open the output file for writing. We use UTF-8 encoding to ensure that any special characters
    # in the BibTeX file are correctly handled and displayed.
    with open(output_file, 'w', encoding='utf-8') as out_file:
        # Open the BibTeX file for reading. Specifying UTF-8 encoding ensures that the script can
        # handle any special characters that may appear in bibliographic entries.
        with open(bibtex_file, 'r', encoding='utf-8') as bibtex_file:
            # Load and parse the BibTeX file. The bibtexparser library is used here to parse the file,
            # which converts the BibTeX entries into a Python dictionary-like structure.
            bib_database = bibtexparser.load(bibtex_file)

        # Loop through each entry in the parsed BibTeX database. Each entry is a dictionary
        # containing bibliographic information such as author, title, journal, and year.
        for entry in bib_database.entries:
            # Write a header to distinguish each entry in the output file.
            out_file.write("\nEntry:\n")
            
            # Extract the author information from the entry. If it is not present,
            # 'No author information' is written instead.
            authors = entry.get('author', 'No author information')
            out_file.write(f"Authors: {authors}\n")

            # Extract the title of the work from the entry. If it is not present,
            # 'No title' is written instead.
            title = entry.get('title', 'No title')
            out_file.write(f"Title: {title}\n")

            # Extract the publication year. If it is not present,
            # 'No publication year' is written instead.
            year = entry.get('year', 'No publication year')
            out_file.write(f"Publication Year: {year}\n")

            # Extract the journal name. If it is not present,
            # 'No journal information' is written instead.
            journal = entry.get('journal', 'No journal information')
            out_file.write(f"Journal: {journal}\n")

            # Additional metadata that does not fall into the above categories
            # is written under 'Other Metadata'.
            out_file.write("Other Metadata:\n")
            for key, value in entry.items():
                # Only include additional metadata that is not author, title, year, or journal.
                if key not in ['author', 'title', 'year', 'journal']:
                    out_file.write(f"{key}: {value}\n")
if __name__ == '__main__':  
    # Example usage: specify the path to your BibTeX file and the desired output file path.
    extract_meta_information('2024-CEE520.bib', 'extracted_metadata.txt')
