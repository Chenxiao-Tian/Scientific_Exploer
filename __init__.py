
# This file makes the directory a Python package# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 22:29:09 2024

@author: ct347
"""

"""
SciNetExplorer Package Initialization.

This package provides tools for analyzing and visualizing the network of scientific papers.
It includes functionality for extracting metadata, linking papers, analyzing text,
and visualizing relationships in the scientific literature.
"""

# Import specific main functions from each step/module for easier access from the package
from .step_1_extract_meta_information import extract_meta_information
from .step_2_manual_linking_of_papers import draw_citation_network
from .step_3_automatic_extraction_of_connections import main_output_3
from .step_4_read_pdf_versions_of_papers import main_output_4
from .step_5_extract_keywords_and_content import main_output_5
from .step_6_link_papers_with_similar_content import main_output_6
from .step_7_analyze_and_visualize_results import main_output_7

# Optionally, initialize anything that needs to be set up when the package is loaded
print("SciNetExplorer loaded. Ready to analyze scientific networks.")
