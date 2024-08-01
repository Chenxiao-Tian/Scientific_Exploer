# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:38:19 2024

@author: ct347
"""

import bibtexparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt

def load_documents(bib_path):
    """
    Load documents from a BibTeX file.

    Parameters:
        bib_path (str): Path to the BibTeX file.

    Returns:
        list: List of dictionaries containing document information.
    """
    with open(bib_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    documents = []
    for entry in bib_database.entries:
        doc_info = {
            'title': entry.get('title', '').replace('{', '').replace('}', ''),
            'year': int(entry.get('year', '0')),
            'keywords': entry.get('keywords', ''),
            'authors': entry.get('author', ''),
            'abstract': entry.get('abstract', '').replace('{', '').replace('}', '')
        }
        documents.append(doc_info)
    return documents

def build_citation_graph(documents):
    """
    Build a citation graph based on document similarity.

    Parameters:
        documents (list): List of dictionaries containing document information.

    Returns:
        nx.DiGraph: Directed graph representing the citation relationships.
    """
    G = nx.DiGraph()
    documents = sorted(documents, key=lambda x: x['year'])  # Ensure sorting by year
    corpus = [doc['keywords'] + ' ' + doc['abstract'] for doc in documents]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(corpus)
    cos_sim = cosine_similarity(X)

    for i, doc in enumerate(documents):
        for j, other_doc in enumerate(documents):
            if doc['year'] > other_doc['year']:  # Ensure only earlier documents can be cited by later documents
                similarity = cos_sim[j, i]  # Note the indexing of cos_sim, from j to i means j cites i
                if similarity > 0.2:  # Set a similarity threshold
                    G.add_edge(other_doc['title'], doc['title'], weight=similarity)

    return G

def visualize_citation_graph(G):
    """
    Visualize the citation graph.

    Parameters:
        G (nx.DiGraph): Directed graph representing the citation relationships.
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.25, iterations=20)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray', arrowsize=20)
    plt.title('Citation Graph by Automatic Extraction of Connections')
    plt.savefig('Citation Graph by Automatic Extraction of Connections')
    plt.show()

def main_output_3(bib_path):
    """
    Main function to load documents, build citation graph, and visualize it.

    Parameters:
        bib_path (str): Path to the BibTeX file.
    """
    documents = load_documents(bib_path)
    G = build_citation_graph(documents)
    visualize_citation_graph(G)

if __name__ == "__main__":
    bib_path = '2024-CEE520.bib'
    main_output_3(bib_path)
