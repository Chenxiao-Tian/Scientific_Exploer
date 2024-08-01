# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:29:20 2024

@author: ct347
"""

import bibtexparser
import PyPDF2
import os
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import community as community_louvain


def load_bibtex(file_path):
    """
    Load BibTeX file and extract relevant information.
    """
    with open(file_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    documents = []
    authors_dict = {}
    citations = []
    for entry in bib_database.entries:
        doc_info = {
            'title': entry.get('title', ''),
            'abstract': entry.get('abstract', ''),
            'keywords': entry.get('keywords', ''),
            'authors': entry.get('author', '').split(' and '),
            'file': entry.get('file', '').split(':')[0] if 'file' in entry else ''
        }
        documents.append(doc_info)
        for author in doc_info['authors']:
            if author not in authors_dict:
                authors_dict[author] = []
            authors_dict[author].append(doc_info['title'])
        if 'citation' in entry:
            for cited in entry.get('citation', '').split(';'):
                citations.append((doc_info['title'], cited.strip()))
    return documents, authors_dict, citations

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """
    text = ""
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() if page.extract_text() else ""
    return text

def build_text_data(documents):
    """
    Build text data for documents.
    """
    text_data = []
    for doc in documents:
        if doc['file']:
            pdf_text = extract_text_from_pdf(doc['file'])
        else:
            pdf_text = ""
        combined_text = f"{doc['abstract']} {doc['keywords']} {pdf_text}"
        text_data.append(combined_text)
    return text_data

def cluster_documents(text_data, n_clusters=3):
    """
    Cluster documents using TF-IDF and KMeans.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(text_data)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    return kmeans.labels_

def create_network_graph(documents, labels):
    """
    Create a network graph of documents.
    """
    G = nx.Graph()
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([doc['abstract'] + " " + doc['keywords'] for doc in documents])
    cos_sim = cosine_similarity(X)
    threshold = 0.2
    for i in range(len(documents)):
        G.add_node(documents[i]['title'], label=labels[i], authors=documents[i]['authors'])
        for j in range(i + 1, len(documents)):
            if cos_sim[i, j] > threshold:
                G.add_edge(documents[i]['title'], documents[j]['title'], weight=cos_sim[i, j])
    return G

def analyze_network(G, save_plots=True):
    """
    Analyze the network graph of documents.
    """
    # Community detection
    partition = community_louvain.best_partition(G, resolution=1.0)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 12))
    cmap = plt.get_cmap('viridis')
    nx.draw_networkx_nodes(G, pos, node_size=70, cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.title('Community Structure in Scientific Paper Network')
    if save_plots:
        plt.savefig('community_structure.png')  # Save the plot as an image
    plt.show()

    # Centrality analysis
    centrality = nx.degree_centrality(G)
    sorted_centrality = sorted(centrality.items(), key=lambda item: item[1], reverse=True)
    print("Top 5 influential papers based on degree centrality:")
    for title, score in sorted_centrality[:5]:
        print(f"{title}: {score}")

    # Draw nodes with highest centrality
    plt.figure(figsize=(12, 12))
    node_color = [centrality[v] * 1000 for v in G]
    nx.draw_networkx(G, pos, node_color=node_color, with_labels=False, node_size=node_color, edge_color="#AAAAAA")
    plt.title('Node Centrality in Scientific Paper Network')
    plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=plt.gca(), orientation='vertical', label='Degree Centrality')
    if save_plots:
        plt.savefig('node_centrality.png')  # Save the plot as an image
    plt.show()

def highlight_connections(G):
    """
    Highlight connections in the network graph.
    """
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.title('Network Graph with Highlighted Connections')
    plt.savefig('highlighted_connections.png')  # Save the plot as an image
    plt.show()

def analyze_community_structure(G):
    """
    Analyze the community structure in the network graph.
    """
    partition = community_louvain.best_partition(G)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    cmap = plt.get_cmap('viridis')
    nx.draw_networkx_nodes(G, pos, node_size=300, cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.title('Network Graph with Community Structure')
    plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), label='Community')
    plt.savefig('community_structure.png')  # Save the plot as an image
    plt.show()

def highlight_key_papers(G, centrality_threshold=0.05):
    """
    Highlight key papers in the network graph based on centrality.
    """
    centrality = nx.degree_centrality(G)
    key_papers = [node for node, centrality_score in centrality.items() if centrality_score > centrality_threshold]
    key_papers_graph = G.subgraph(key_papers)
    pos = nx.spring_layout(key_papers_graph)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(key_papers_graph, pos, node_size=300, node_color='skyblue')
    nx.draw_networkx_edges(key_papers_graph, pos, alpha=0.5)
    plt.title('Network Graph with Key Papers Highlighted')
    plt.savefig('key_papers_highlighted.png')  # Save the plot as an image
    plt.show()

def highlight_influential_authors(G, degree_threshold=3):
    """
    Highlight influential authors in the network graph based on degree centrality.
    """
    influential_authors = [author for author, degree in G.degree() if degree >= degree_threshold]
    influential_authors_graph = G.subgraph(influential_authors)
    pos = nx.spring_layout(influential_authors_graph)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(influential_authors_graph, pos, node_size=300, node_color='skyblue')
    nx.draw_networkx_edges(influential_authors_graph, pos, alpha=0.5)
    author_labels = {author: author.split()[-1] for author in influential_authors}
    nx.draw_networkx_labels(influential_authors_graph, pos, labels=author_labels, font_size=10, font_color='black')
    plt.title('Network Graph with Influential Authors Highlighted')
    plt.savefig('influential_authors_highlighted.png')  # Save the plot as an image
    plt.show()

def analyze_influential_authors(G, degree_threshold=3):
    """
    Analyze influential authors in the network graph based on degree centrality.
    """
    influential_authors = [author for author, degree in G.degree() if degree >= degree_threshold]
    print("Influential Authors:")
    for author in influential_authors:
        print(author)
     
    
    influential_authors_graph = G.subgraph(influential_authors)

    pos = nx.spring_layout(influential_authors_graph)
    plt.figure(figsize=(10, 6))

  
    nx.draw_networkx_nodes(influential_authors_graph, pos, node_size=300, node_color='skyblue')
    nx.draw_networkx_edges(influential_authors_graph, pos, alpha=0.5)
    author_labels = {author: author.split()[-1] for author in influential_authors}
    nx.draw_networkx_labels(influential_authors_graph, pos, labels=author_labels, font_size=10, font_color='black')

    plt.title('Network Graph with Influential Authors Highlighted')
    plt.savefig('Network Graph with Influential Authors Highlighted')  # Save the plot as an image
    plt.show()

def identify_major_research_clusters(G):
    """
    Identify major research clusters in the network graph.
    """
    partition = community_louvain.best_partition(G)
    cluster_colors = [partition[node] for node in G.nodes()]
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_size=300, cmap=plt.cm.viridis, node_color=cluster_colors)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.title('Network Graph with Major Research Clusters Identified')
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), label='Research Cluster')
    plt.savefig('major_research_clusters.png')  # Save the plot as an image
    plt.show()

def main_output_7(bib_path):
    """
    Main function to execute the analysis.
    """
    documents, authors_dict, citations = load_bibtex(bib_path)
    text_data = build_text_data(documents)
    labels = cluster_documents(text_data)
    G = create_network_graph(documents, labels)
    analyze_network(G)
    highlight_connections(G)
    highlight_key_papers(G)
    highlight_influential_authors(G)
    analyze_influential_authors(G)
    analyze_community_structure(G)
    identify_major_research_clusters(G)

if __name__ == "__main__":
    bib_path = '2024-CEE520.bib'  # Set this to your bib file path
    main_output_7(bib_path)
