# Metadata Viewer

A simple tool for viewing GitHub repository metadata through the GitHub API.

## Features

* Repository metadata

  * Displays repository name
  * Displays repository owner
  * Displays repository description
  * Displays repository visibility
  * Displays default branch
  * Shows stars, forks, issues and watchers
  * Shows repository language
  * Shows repository license
  * Shows creation, update and push dates
  * Displays repository topics

## Usage

Run RepoRecon:

```bash
python main.py
```

Select:

```text
REPOSITORY TOOLS
```

Then select:

```text
Metadata Viewer
```

Enter a GitHub repository URL:

```text
Enter repository URL: https://github.com/user/repository
```

The tool queries the GitHub API and displays the available metadata.

## Output

The tool displays:

```text
Name
Owner
Description
Visibility
Default branch
```

Repository statistics:

```text
Stars
Forks
Open issues
Watchers
```

Repository information:

```text
Language
License
Created
Last updated
Last pushed
```

If the repository has topics, they are also displayed.

## GitHub API

The tool uses the GitHub REST API.

A GitHub API token can be provided through:

```text
GITHUB_API_TOKEN
```

The token is loaded from the environment using `python-dotenv`.

## Requirements

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Disclaimer

This tool is intended for educational purposes and legitimate OSINT research.

Only use RepoRecon against repositories and information that you are authorised to investigate.

[Back to Repository Tools](../repo_tools.md)
