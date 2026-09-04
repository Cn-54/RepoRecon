# Repo-Recon

A simple Python CLI multitool for performing GitHub repository reconnaissance and OSINT.

## Features

* Repository auditing

  * Extracts commit information
  * Finds unique authors and emails
  * Counts commits per author
  * Calculates author commit percentages
  * Finds first and last commit dates
  * Flags potential personal emails

* Repository metadata

  * Gets repository information through the GitHub API
  * Displays repository owner and description
  * Shows stars, forks, issues and watchers
  * Shows repository language and license
  * Shows creation, update and push dates
  * Displays repository topics

* Reverse username searching

  * Checks usernames across multiple websites
  * Sites can be added or removed through `sites.txt`
  * Shows found, not found and error results
  * Displays total search statistics

## Structure

Tools are separated into different categories:

* `repo/`

  * Tools for GitHub repository reconnaissance

* `user/`

  * Tools for GitHub user reconnaissance

* `misc/`

  * Tools that do not specifically belong to repositories or users

Each tool uses a `run()` function which allows RepoRecon to automatically find and load tools from their respective directories.

## Usage

Run the program with:

```
python main.py
```

A menu will appear allowing you to navigate between the available tools.

Repository tools are located on the first page.

User tools are located on the second page.

Miscellaneous tools are located on the third page.

## Requirements

```
pip install -r requirements.txt
```

Git must also be installed and available in your PATH.

## Files

```
RepoRecon/
├── main.py
├── sites.txt
├── requirements.txt
├── README.md
└── tools/
    ├── repo/
    │   ├── repo_audit.py
    │   └── metadata_viewer.py
    │
    ├── user/
    │
    ├── misc/
    │   └── username_search.py
    │
    └── utils/
        └── _clear_terminal.py
```

## Adding Tools

Tools can be added by creating a Python file inside the appropriate directory.

For example:

```
tools/repo/branch_analysis.py
```

The file must contain a `run()` function:

```
def run():
    # Tool code
```

RepoRecon will automatically detect the file and add it to the menu.

Files beginning with `_` are ignored by the tool loader and can be used for utility modules.

## Sites

Username searching uses `sites.txt` to store the websites that are checked.

Sites are separated into categories and use `{}` as the username placeholder.

For example:

```
https://github.com/{}
https://www.instagram.com/{}
https://www.reddit.com/user/{}
```

Sites can be added or removed without changing the Python code.

## Disclaimer

This tool is intended for educational purposes and legitimate OSINT research.

Only use RepoRecon against repositories, accounts and information that you are authorised to investigate.
