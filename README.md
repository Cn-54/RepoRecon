# Repo-Recon

A simple Python CLI multitool for performing GitHub repository reconnaissance and OSINT.

## Features

* Repository auditing

  * Extracts commit information
  * Finds unique authors and emails
  * Counts commits per author
  * Flags potential personal emails
* Reverse username searching

  * Checks usernames across multiple websites
  * Sites can be added or removed through `sites.txt`
* Repository + username search

  * Extracts author names from a repository
  * Searches those names across the configured sites

## Usage

Run the program with:

```bash
python main.py
```

A menu will appear allowing you to select the tool you want to use.

## Requirements

```bash
pip install -r requirements.txt
```

Git must also be installed and available in your PATH.

## Files

```text
RepoRecon/
├── main.py
├── sites.txt
├── requirements.txt
├── README.md
└── tools/
    ├── repo_audit.py
    └── username_search.py
```

## Disclaimer

This tool is intended for educational purposes and legitimate OSINT research.
