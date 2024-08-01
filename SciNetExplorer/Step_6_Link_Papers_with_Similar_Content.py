# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 07:44:02 2024

@author: ct347
"""

import bibtexparser
import PyPDF2
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

def load_bibtex(file_path):
    """Parse a .bib file and extract necessary information"""
    with open(file_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    documents = []
    for entry in bib_database.entries:
        doc_info = {
            'title': entry.get('title', ''),
            'abstract': entry.get('abstract', ''),
            'keywords': entry.get('keywords', ''),
            'file': entry.get('file', '').split(':')[0]  # Assuming file path is before ':'
        }
        documents.append(doc_info)
    return documents

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    text = ""
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() if page.extract_text() else ""
    return text

def create_cluster_graph(documents, labels):
    """Create a graph of the document clusters"""
    G = nx.Graph()
    for doc, label in zip(documents, labels):
        G.add_node(doc['title'], label=label)

    # Assign colors to nodes
    color_map = []
    for node in G:
        node_label = G.nodes[node]['label']
        # Choose colors based on cluster labels
        if node_label == 0:
            color_map.append('red')
        elif node_label == 1:
            color_map.append('blue')
        else:
            color_map.append('green')

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # Use spring layout for aesthetics and distinction
    nx.draw(G, pos, node_color=color_map, with_labels=True, font_weight='bold', node_size=5000)
    plt.title('Cluster Graph')
    plt.show()

def main_output_6(bib_path, output_path):
    """Main function to load data, process it, and output cluster results"""
    documents = load_bibtex(bib_path)
    text_data = []

    for doc in documents:
        pdf_text = extract_text_from_pdf(doc['file'])
        combined_text = f"{doc['abstract']} {doc['keywords']} {pdf_text}"
        text_data.append(combined_text)

    # Text vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(text_data)

    # Clustering analysis
    kmeans = KMeans(n_clusters=3, random_state=42)  # Assume we divide into 3 clusters
    kmeans.fit(X)
    labels = kmeans.labels_

    # Create and display a cluster graph
    create_cluster_graph(documents, labels)

    # Organize documents by clusters and write to file
    cluster_dict = defaultdict(list)
    for title, label in zip([doc['title'] for doc in documents], labels):
        cluster_dict[label].append(title)

    with open(output_path, 'w') as f:
        for cluster in sorted(cluster_dict):
            f.write(f"Cluster {cluster}:\n")
            for title in cluster_dict[cluster]:
                f.write(f"- {title}\n")
            f.write("\n")

if __name__ == "__main__":
    bib_path = '2024-CEE520.bib'  # Set to your .bib file path
    output_path = 'output_Step_6.txt'  # Set to your output text file path
    main_output_6(bib_path, output_path)
