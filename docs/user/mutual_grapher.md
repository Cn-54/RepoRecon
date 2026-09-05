# Mutuals Grapher

A tool for building an interactive graph of mutual GitHub relationships.

## Features

* GitHub user reconnaissance

  * Finds followers
  * Finds following accounts
  * Finds mutual followers/following
  * Builds relationships between accounts
  * Supports configurable graph depth
  * Supports configurable mutuals per account
  * Generates an interactive HTML graph

## Usage

Run RepoRecon:

```bash
python main.py
```

Navigate to:

```text
USER TOOLS
```

Then select:

```text
Mutuals Grapher
```

The tool asks for:

```text
GitHub username:
Maximum depth:
Maximum mutuals per account:
```

Example:

```text
GitHub username: example
Maximum depth: 2
Maximum mutuals per account: 5
```

## Graph

The tool finds accounts that both follow the target account and are followed by the target account.

These mutual relationships are represented as graph edges.

Each account can contain:

* Username
* Email
* Public repositories
* Followers
* Following

Hovering over a node displays this information.

## Output

The graph is saved as an interactive HTML file:

```text
outputs/<username>-connections.html
```

The graph can be opened in a web browser.

## Graph Controls

The generated graph supports:

* Hovering over nodes
* Navigation buttons
* Keyboard controls
* Physics-based graph movement

## Configuration

The GitHub API token is loaded from:

```text
GITHUB_API_TOKEN
```

The token is read using `python-dotenv`.

## Requirements

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Disclaimer

This tool is intended for educational purposes and legitimate OSINT research.

Only use RepoRecon against accounts and information that you are authorised to investigate.

[Back to User Tools](../user_tools.md)
