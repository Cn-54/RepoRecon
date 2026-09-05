# Relationship Grapher

A tool for building an interactive graph of GitHub user relationships.

## Features

* GitHub user reconnaissance

  * Gets GitHub user information
  * Finds followers
  * Finds following accounts
  * Builds relationships between accounts
  * Supports configurable graph depth
  * Supports configurable connections per account
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
Relationship Grapher
```

The tool asks for:

```text
GitHub username:
Maximum depth:
Maximum connections per account:
```

Example:

```text
GitHub username: example
Maximum depth: 2
Maximum connections per account: 5
```

## Graph

The tool uses GitHub followers and following relationships to build the graph.

Each account is represented as a node.

Relationships are represented as edges.

The graph contains information such as:

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
