# Get Articles List

## Description
Get Papers List is a Python project that fetches research papers from PubMed based on specified queries. It retrieves PubMed IDs, extracts paper details, and saves the results to a CSV file.

## Code Organization
In the file Scripts/get_papers_list.py there is the main function to be executed to run the application. This main function calls the functionalities from get_papers_list/fetch_papers.py. fetch_papers.py is the file that fetches research papers based on a user-specified query.

## Dependencies
- requests (>=2.32.3,<3.0.0)
- pandas (>=2.2.3,<3.0.0)
- argparse (>=1.4.0,<2.0.0)


## Installation & Usage
To install the project dependencies, use Poetry:

```bash
git clone https://github.com/Ashoksanaka/Article_Fetcher.git
```
```bash
cd Article_Fetcher/
```
```bash
poetry install
```
After installing the necessary dependencies run below command to run the script.
```bash
python3 -m Scripts.get_papers_list "<Topic name>" -f <output file name>
```
You can also use the arguments along with command. The arguments are:
```bash
-h or --help:    Display Usage instructions
-d or --debug: print debug information while execution
-f or --file: specify the file name to save the results. If this option is not provided, print the output to the console
```
