# Repo Audit

A simple tool for analysing the commit history of a Git repository.

## Features

* Repository auditing

  * Clones a Git repository into a temporary directory
  * Extracts commit information
  * Finds unique authors and emails
  * Counts commits per author
  * Calculates author commit percentages
  * Finds first and last commit dates
  * Flags non-GitHub email addresses

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
Repo Audit
```

Enter the repository URL when prompted:

```text
Enter repository URL: https://github.com/user/repository.git
```

The repository is cloned temporarily and removed automatically after the audit.

## Output

The tool displays:

* Repository URL
* Total commits
* Author names
* Author emails
* Commit counts
* First commit date
* Last commit date
* Commit percentage
* Potential personal email addresses

## Email Detection

GitHub-generated noreply addresses are treated as GitHub emails:

```text
user@users.noreply.github.com
```

Other email addresses are flagged as:

```text
[!] Non github email
```

## Requirements

Git must be installed and available in your PATH.

Python dependencies are installed with:

```bash
pip install -r requirements.txt
```

## Disclaimer

This tool is intended for educational purposes and legitimate OSINT research.

Only use RepoRecon against repositories and information that you are authorised to investigate.
