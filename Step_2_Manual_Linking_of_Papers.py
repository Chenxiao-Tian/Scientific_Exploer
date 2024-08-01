from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import bibtexparser
import networkx as nx
import matplotlib.pyplot as plt

def get_references(doi):
    """
    Get references for a given DOI using the CrossRef API.

    Parameters:
        doi (str): The DOI of the paper.

    Returns:
        list: A list of DOIs of papers referenced by the given DOI.
    """
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        references = data.get('message', {}).get('reference', [])
        return [ref.get('DOI') for ref in references if 'DOI' in ref]
    return []
def draw_citation_network(file_path):
    # Read the BibTeX file
    with open('2024-CEE520.bib', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    # Initialize a directed graph and reference cache
    G = nx.DiGraph()
    reference_cache = {}
    doi_to_key = {entry.get('doi'): entry.get('ID') for entry in bib_database.entries if 'doi' in entry}  # Mapping DOI to citationkey
    
    # Use a thread pool to get reference information for all papers
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_entry = {executor.submit(get_references, entry.get('doi')): entry for entry in bib_database.entries if 'doi' in entry}
        for future in as_completed(future_to_entry):
            entry = future_to_entry[future]
            doi = entry.get('doi')
            citationkey = entry.get('ID')  # Assuming 'ID' is the field for citationkey
            try:
                references = future.result()
                reference_cache[citationkey] = references
                G.add_node(citationkey)  # Use citationkey instead of doi
            except Exception as e:
                print(f"Error retrieving references for DOI {doi}: {e}")
    
    # Add directed edges based on the reference cache
    for citing_key, refs in reference_cache.items():
        for ref_doi in refs:
            if ref_doi in doi_to_key:  # Ensure the referenced DOI is in our list
                cited_key = doi_to_key[ref_doi]
                G.add_edge(citing_key, cited_key)  # Add an edge from the citing document to the cited document
    
    # Visualize the directed graph
    plt.figure(figsize=(10, 8))
    nx.draw(G, with_labels=True, node_size=2000, node_color="lightblue", font_size=8)
    plt.title('Citation Graph by Direct Citation Relationship')
    plt.savefig('Citation Graph by Direct Citation Relationship')
    plt.show()
if __name__ == '__main__':    
   file_path='2024-CEE520.bib'
   draw_citation_network(file_path)
