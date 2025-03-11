# get_papers_list/fetch_papers.py

import requests
import re
import pandas as pd
from typing import List, Dict

# List of pharmaceutical/biotech companies (expand as needed)
COMPANIES = [
    "Pfizer", "Johnson & Johnson", "Merck", "Bristol Myers Squibb", 
    "AstraZeneca", "GSK", "Novartis", "Sanofi", "Roche", "AbbVie"
]

# Function to fetch PubMed IDs based on the query
def fetch_pubmed_ids(query: str, max_results: int = 100) -> List[str]:
    # PubMed search URL
    PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "usehistory": "y",
        "retmode": "xml"
    }
    response = requests.get(PUBMED_BASE_URL, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching PubMed data: {response.status_code}")
    
    # Parse XML response to extract PubMed IDs
    xml_data = response.text
    ids = re.findall(r"<Id>(\d+)</Id>", xml_data)
    return ids


# Function to fetch paper details from PubMed using PubMed IDs
def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict[str, str]]:
    PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    ids_str = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml",
        "rettype": "abstract"
    }
    
    response = requests.get(PUBMED_FETCH_URL, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching paper details: {response.status_code}")
    
    xml_data = response.text
    papers = []
    
    # Extract paper details from the XML response
    for paper in re.finditer(r"<PubmedArticle>(.*?)</PubmedArticle>", xml_data, re.DOTALL):
        article = paper.group(1)
        
        # Extract PubMed ID, title, and publication date
        pubmed_id = re.search(r"<PMID Version=\"1\">(\d+)</PMID>", article).group(1)
        title = re.search(r"<ArticleTitle>(.*?)</ArticleTitle>", article).group(1)
        
        # Extract publication date
        pub_date_match = re.search(r"<PubDate><Year>(.*?)</Year><Month>(.*?)</Month><Day>(.*?)</Day></PubDate>", article)
        pub_date = f"{pub_date_match.group(1)}-{pub_date_match.group(2)}-{pub_date_match.group(3)}" if pub_date_match else "Unknown"
        
        # Extract authors and affiliations
        authors = re.findall(r"<Author>(.*?)</Author>", article, re.DOTALL)
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = None
        
        for author in authors:
            last_name = re.search(r"<LastName>(.*?)</LastName>", author).group(1)
            first_name = re.search(r"<ForeName>(.*?)</ForeName>", author).group(1)
            affiliation = re.search(r"<Affiliation>(.*?)</Affiliation>", author).group(1)
            
            # Check if the author is affiliated with a company
            if any(company in affiliation for company in COMPANIES):
                non_academic_authors.append(f"{first_name} {last_name}")
                company_affiliations.extend([company for company in COMPANIES if company in affiliation])
            
            # Check if it's the corresponding author
            if re.search(r"<CorrespondingAuthor>", author):
                corresponding_email = re.search(r"<Email>(.*?)</Email>", author).group(1) if re.search(r"<Email>(.*?)</Email>", author) else None
        
        paper_details = {
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors),
            "Company Affiliation(s)": ", ".join(set(company_affiliations)),
            "Corresponding Author Email": corresponding_email or "N/A"
        }
        papers.append(paper_details)

    return papers


# Function to save the paper details to a CSV file
def save_to_csv(papers: List[Dict[str, str]], output_file: str) -> None:
    df = pd.DataFrame(papers)
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")