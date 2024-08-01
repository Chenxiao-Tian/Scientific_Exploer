# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 22:31:54 2024

@author: ct347
"""

import unittest
import os

from SciNetExplorer.step_1_extract_meta_information import extract_meta_information
from SciNetExplorer.step_2_manual_linking_of_papers import link_papers_manually
from SciNetExplorer.step_3_automatic_extraction_of_connections import extract_connections
from SciNetExplorer.step_4_read_pdf_versions_of_papers import read_pdf
from SciNetExplorer.step_5_extract_keywords_and_content import extract_keywords
from SciNetExplorer.step_6_link_papers_with_similar_content import link_similar_papers
from SciNetExplorer.step_7_analyze_and_visualize_results import analyze_results

class TestSciNetExplorerSteps(unittest.TestCase):

    def setUp(self):
        # Setup paths and example data for testing
        self.example_bib_path = 'example.bib'  # Ensure this path points to a sample BibTeX file
        self.example_pdf_path = 'example.pdf'  # Ensure this path points to a sample PDF file

    def test_extract_meta_information(self):
        """Test extracting metadata from a BibTeX file."""
        metadata = extract_meta_information(self.example_bib_path)
        self.assertIsInstance(metadata, list)
        self.assertGreater(len(metadata), 0)

    def test_link_papers_manually(self):
        """Test manual linking of papers."""
        connections = link_papers_manually()
        self.assertIsInstance(connections, list)

    def test_extract_connections(self):
        """Test automatic extraction of connections from text."""
        connections = extract_connections(self.example_bib_path)  # Assuming this takes a path or similar input
        self.assertIsInstance(connections, list)

    def test_read_pdf(self):
        """Test reading text from a PDF file."""
        text = read_pdf(self.example_pdf_path)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)

    def test_extract_keywords(self):
        """Test keyword extraction from text."""
        keywords = extract_keywords("This is a sample text for testing keyword extraction.")
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)

    def test_link_similar_papers(self):
        """Test linking papers based on content similarity."""
        links = link_similar_papers(['paper1', 'paper2'], [{'text': 'sample text'}, {'text': 'similar text'}])
        self.assertIsInstance(links, list)

    def test_analyze_results(self):
        """Test analysis and visualization of results."""
        # Assuming this function does not return but modifies or outputs data
        self.assertIsNone(analyze_results())

if __name__ == '__main__':
    unittest.main()

