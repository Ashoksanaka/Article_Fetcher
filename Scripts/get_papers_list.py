# scripts/get_papers_list.py

import argparse
import os

from get_papers_list.fetch_papers import fetch_pubmed_ids, fetch_paper_details, save_to_csv

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Fetch and filter PubMed papers based on query.")
    parser.add_argument("query", help="Query to search for papers")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-f", "--file", help="Output CSV file")
    
    args = parser.parse_args()

    # Enable debug mode if specified
    if args.debug:
        print("Debug mode enabled.")
        print(f"Query: {args.query}")
    
    try:
        # Fetch PubMed IDs based on the user query
        pubmed_ids = fetch_pubmed_ids(args.query)
        
        if not pubmed_ids:
            print("No papers found for the given query.")
            return

        # Fetch paper details (title, authors, publication date, etc.) using the PubMed IDs
        papers = fetch_paper_details(pubmed_ids)
        
        # Save the results to a CSV file if the --file argument is passed, else print to console
        if args.file:
            save_to_csv(papers, args.file)
        else:
            for paper in papers:
                print(paper)
    
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
