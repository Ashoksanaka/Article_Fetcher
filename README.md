# Get Papers List

## Description
Get Papers List is a Python project that fetches research papers from PubMed based on specified queries. It retrieves PubMed IDs, extracts paper details, and saves the results to a CSV file.

## Installation
To install the project dependencies, use Poetry:

```bash
poetry install
```

## Usage
1. **Fetch PubMed IDs**:
   Use the `fetch_pubmed_ids` function to search for papers based on a query.

2. **Fetch Paper Details**:
   Use the `fetch_paper_details` function to retrieve details of papers using their PubMed IDs.

3. **Save Results**:
   Use the `save_to_csv` function to save the fetched paper details to a CSV file.

## Dependencies
- requests (>=2.32.3,<3.0.0)
- pandas (>=2.2.3,<3.0.0)
- argparse (>=1.4.0,<2.0.0)

## Author
- Ashoksanaka (ashoksanaka116@gmail.com)

## License
This project is licensed under the MIT License.
