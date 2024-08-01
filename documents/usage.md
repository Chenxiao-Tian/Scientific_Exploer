# Usage Guide for SciNetExplorer

## Introduction

`SciNetExplorer` is a sophisticated Python package designed for academics and researchers. It automates the processing of BibTeX files, linking scholarly papers, extracting content from PDFs, analyzing connections, and visualizing data. This package streamlines the management of bibliographic data, enhances the understanding of literature connections, and aids in the visualization of academic networks.

### Installation

### Installation

#### Step 1: Clone the Repository
First, you need to clone the repository from GitHub to your local machine. You can do this using Git command-line tools or directly through an IDE that supports Git operations. Here’s how to do it via the command line:

Open your command line interface (Terminal on macOS and Linux, Command Prompt or PowerShell on Windows).
Navigate to the directory where you want to clone the repository.
Run the Git clone command with the URL of the repository:

```bash
git clone https://github.com/cis-teaching/challenge_2_SciNetExplorer.git
```
####  Step 2: Set Up a Python Environment
It's a good practice to use a virtual environment for Python projects to manage dependencies:

Navigate into the project directory:

```bash

cd challenge_2_SciNetExplorer
```
Create a virtual environment (replace venv with your desired environment name):

```bash
python -m venv venv
```

Activate the virtual environment:
On Windows:

```bash
.\venv\Scripts\activate
```
On macOS and Linux:

```bash
source venv/bin/activate
```
#### Step 3: Install Dependencies
Install the project dependencies which are usually listed in a requirements.txt file:

```bash
pip install -r requirements.txt
```
#### Step 4: Install the Package
If the package is meant to be installed locally (assuming it includes a setup.py file):


```bash
pip install .
```

This command will install the current package and all its dependencies.
#### Step 5: Post-Installation
For the later module 5 analysis, after installing the SciNetExplorer package, you need to download the necessary spaCy language model. Run the following command:

```bash
python -m spacy download en_core_web_sm
```
#### Specific Usage for Each Python Model
### 1. Extract Meta Information
**File:** `Step_1_Extract_Meta_Information.py`

#### Description
This module extracts meta-information from Zotero-generated BibTeX files, such as author names, paper titles, publication years, journals, and other relevant metadata essential for categorizing scientific papers.

#### Functionality
Processes a BibTeX file to extract metadata necessary for further analysis in subsequent steps.

#### Usage
```python
from Step_1_Extract_Meta_Information import extract_meta_information
# Example usage: specify the path to your BibTeX file and the desired output file path.
extract_meta_information('2024-CEE520.bib', 'extracted_metadata.txt')
```

Note: if it's in a windows powershell environment you could run command:
```
python -c "from Step_1_Extract_Meta_Information import extract_meta_information; extract_meta_information('2024-CEE520.bib', 'extracted_metadata.txt')"
```

### 2. Manual Linking of Papers
**File:** `Step_2_Manual_Linking_of_Papers.py`

#### Description
This module allows users to manually create a citation network by linking papers that reference each other. It utilizes metadata extracted from the previous step to establish connections between scientific papers based on citations.

#### Functionality
The module takes metadata extracted from Step 1 and provides functionality for users to manually link papers by their identifiers, thus building the citation network structure needed for further analysis.

#### Usage
# Read the BibTeX file
```python
from Step_2_Manual_Linking_of_Papers import draw_citation_network
file_path='2024-CEE520.bib'
draw_citation_network(file_path)
```
Note: if it's in a windows powershell environment you could run command:
```
python -c "from Step_2_Manual_Linking_of_Papers import draw_citation_network
file_path='2024-CEE520.bib'
draw_citation_network(file_path)"
```
### 3. Automatic Extraction of Connections
**File:** `Step_3_Automatic_Extraction_of_Connections.py`

#### Description
This module attempts to automate the extraction of citation connections directly from the text of scientific papers, thereby enhancing the network of citations without manual input. It analyzes the textual content to detect and extract references and citations among papers.

#### Functionality
Automatically processes textual data to identify and extract citation links, integrating these into the citation network created in previous steps. It leverages advanced text analysis techniques to recognize citation patterns and extract relevant information.

#### Usage
```python
from Step_3_Automatic_Extraction_of_Connections import main_output_3
bib_path = '2024-CEE520.bib'
main_output_3(bib_path)
```

Note: if it's in a windows powershell environment you could run command:
```
python -c "from Step_3_Automatic_Extraction_of_Connections import main_output_3
bib_path = '2024-CEE520.bib'
main_output_3(bib_path)"
```
### 4. Read PDF Versions of Papers
**File:** `Step_4_Read_PDF_Versions_of_Papers.py`

#### Description
This module integrates PDF parsing capabilities to extract text from the full versions of scientific papers, including the main body, references, and any annexes or appendices. It is designed to handle complex layouts and extract readable text that can be used in further analysis.

#### Functionality
Uses PDF parsing tools to read and extract the textual content from PDF files of scientific papers. This module helps in preparing the textual data for keyword extraction, citation detection, and content analysis.

#### Usage
```python
from Step_4_Read_PDF_Versions_of_Papers import main_output_4
bib_file_path = '2024-CEE520.bib'
output_dir = 'Step_4_Output'
main_output_4(bib_file_path,output_dir)
```

Note: if it's in a windows powershell environment you could run command:
```
python -c "from Step_4_Read_PDF_Versions_of_Papers import main_output_4
bib_file_path = '2024-CEE520.bib'
output_dir = 'Step_4_Output'
main_output_4(bib_file_path,output_dir)"
```
### 5. Extract Keywords and Content
**File:** `Step_5_Extract_Keywords_and_Content.py`

#### Description
This module utilizes natural language processing (NLP) techniques to extract keywords, phrases, and overall content from the papers. It is designed to identify the main topics, methodologies, and research outcomes discussed in the papers, which is crucial for understanding the thematic connections among scientific literature.

#### Functionality
Applies advanced NLP methods to process the extracted text and identify significant keywords and phrases. This information is used to understand the focus and scope of the research papers and can aid in linking papers with similar content.

#### Usage
```python
from Step_5_Extract_Keywords_and_Content import main_output_5
bib_file_path = '2024-CEE520.bib'
output_dir = 'step_5_Output' 
main_output_5(bib_file_path, output_dir)
```

Note: if it's in a windows powershell environment you could run command:
```
python -c "from Step_5_Extract_Keywords_and_Content import main_output_5
bib_file_path = '2024-CEE520.bib'
output_dir = 'step_5_Output' 
main_output_5(bib_file_path, output_dir)"
```
### 6. Link Papers with Similar Content
**File:** `Step_6_Link_Papers_with_Similar_Content.py`

#### Description
This module implements algorithms to identify and link papers with similar content, extending beyond direct citations to establish thematic and conceptual connections. It helps build a more comprehensive understanding of how scientific ideas and findings are interrelated across different papers.

#### Functionality
Compares keywords and content extracted from scientific papers to find similarities that indicate thematic or conceptual connections. This facilitates the creation of a network where papers are linked not just by citations but also by shared content and topics.

#### Usage
```python
from Step_6_Link_Papers_with_Similar_Content import main_output_6
bib_path = '2024-CEE520.bib'  # Set to your .bib file path
output_path = 'output_Step_6.txt'  # Set to your output text file path
main_output_6(bib_path, output_path)
```
Note: if it's in a windows powershell environment you could run command:
```
python -c "from Step_6_Link_Papers_with_Similar_Content import main_output_6
bib_path = '2024-CEE520.bib'  # Set to your .bib file path
output_path = 'output_Step_6.txt'  # Set to your output text file path
main_output_6(bib_path, output_path)"
```
### 7. Analyze and Visualize Results
**File:** `Step_7_Analyze_and_Visualize_Results.py`

#### Description
This module uses network analytics to analyze the resulting network of scientific papers, identifying key papers, influential authors, and major research clusters. It incorporates visualization tools to provide graphical representations of the network, highlighting connections, community structures, and other relevant network properties.

#### Functionality
Applies network analysis techniques to the linked network of papers to uncover structural insights such as centrality, connectivity, and community clusters. It then visualizes these networks using various graphical representations to make the data understandable and accessible.

#### Usage
```python
from Step_7_Analyze_and_Visualize_Results import main_output_7
bib_path = '2024-CEE520.bib'  # Set this to your bib file path
main_output_7(bib_path)
```
Note: if it's in a windows powershell environment you could run command:
```
python -c "from Step_7_Analyze_and_Visualize_Results import main_output_7
bib_path = '2024-CEE520.bib'  # Set this to your bib file path
main_output_7(bib_path)"
```

### Data Output:
The package supports exporting data in various formats, enabling integration with data analysis tools and further processing in other software.

### Contributing
Contributions to SciNetExplorer are welcome! If you have ideas for improvements or have identified bugs, please refer to the CONTRIBUTING.md file for guidelines on how to contribute effectively.

### License
SciNetExplorer is licensed under the MIT license. This license allows you to use, modify, and distribute the software freely as long as proper credit is given to the original authors.

### Support
For support, query resolution, or to report issues, please visit the GitHub issues page of the SciNetExplorer repository or contact the maintainer at ct3471@princeton.edu.

### More Information
For more detailed documentation, examples, and API references, please refer to the official documentation hosted on GitHub Pages or the docs directory within the project repository.
