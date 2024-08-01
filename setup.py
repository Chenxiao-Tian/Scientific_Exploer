from setuptools import setup, find_packages

setup(
    name='SciNetExplorer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'bibtexparser',
        'PyPDF2',
        'pdfplumber',
        'matplotlib',
        'networkx',
        'scikit-learn',
        'spacy',
        'yake',
        'community', 
        'python-louvain'
    ],
    author='Chenxiao Tian',
    author_email='ct3471@princeton.edu',
    description='A package for analyzing and visualizing scientific paper networks',
    keywords='scientific papers analysis visualization network',
    url='https://github.com/cis-teaching/challenge_2_SciNetExplorer',  # Optional project URL
)

