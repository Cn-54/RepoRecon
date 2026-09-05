# Repo-Recon

A simple Python CLI multitool for performing GitHub repository reconnaissance and OSINT.

## Features

* Repository auditing

  * Extracts commit information
  * Finds unique authors and emails
  * Counts commits per author
  * Shows first and last commit dates
  * Shows commit percentage per author
  * Flags non-GitHub emails

* Repository metadata

  * Gets repository information through the GitHub API
  * Displays repository owner and description
  * Shows repository visibility and default branch
  * Shows stars, forks, issues and watchers
  * Shows repository language and license
  * Shows creation, update and push dates
  * Displays repository topics

* Reverse username searching

  * Checks usernames across multiple websites
  * Shows found, not found and error results
  * Sites can be added or removed through `sites.txt`

* User relationship graphing

  * Builds graphs from GitHub followers and following
  * Supports configurable graph depth and connections
  * Displays user information on graph nodes
  * Generates interactive HTML graphs

* Mutual relationship graphing

  * Finds mutual followers and following
  * Supports configurable graph depth and connections
  * Displays user information on graph nodes
  * Generates interactive HTML graphs

## Usage

Create a virtual environment with:

```bash
python -m venv .venv
```

Activate the virtual environment with:

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

Install the requirements with:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory and add your GitHub API token:

```text
GITHUB_API_TOKEN=your_token_here
```

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

A GitHub API token is required for the repository metadata and user graphing tools.

## Files

```text
RepoRecon/
├── main.py
├── sites.txt
├── requirements.txt
├── README.md
├── .env
└── tools/
    ├── repo/
    │   ├── repo_audit.py
    │   └── metadata_viewer.py
    │
    ├── user/
    │   ├── mutuals_grapher.py
    │   └── relationship_grapher.py
    │
    ├── misc/
    │   └── username_search.py
    │
    └── utils/
        └── _clear_terminal.py
```

The `.env` file should not be committed to the repository.

Interactive graph results are saved to the `outputs/` directory as HTML files.

## Disclaimer

This tool is intended for educational purposes and legitimate OSINT research.
Only use RepoRecon against repositories, accounts and information that you are authorised to investigate.
