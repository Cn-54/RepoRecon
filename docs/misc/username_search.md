# Username Search

A simple tool for searching for a username across multiple websites.

## Features

* Username searching

  * Checks usernames across multiple websites
  * Uses `sites.txt` to store websites
  * Shows found accounts
  * Shows accounts that were not found
  * Shows errors
  * Displays search statistics

## Usage

Run RepoRecon:

```bash
python main.py
```

Navigate to:

```text
MISC
```

Then select:

```text
Username Search
```

Enter a username:

```text
Enter username: example
```

The tool will check every website listed in `sites.txt`.

## Sites

Websites are stored in:

```text
sites.txt
```

Each site must contain `{}` where the username should be inserted.

Example:

```text
https://github.com/{}
https://www.instagram.com/{}
https://www.reddit.com/user/{}
```

Sites can be added or removed without changing the Python code.

## Output

The tool displays:

```text
Sites checked
Accounts found
Not found
Errors
```

Found accounts are displayed with their URL:

```text
[+] https://example.com/example
```

## How It Works

For each site, RepoRecon:

1. Inserts the username into the URL.
2. Sends an HTTP request.
3. Checks the response status.
4. Checks whether the username appears on the returned page.
5. Records the result.

A `404` response is treated as not found.

Other failed requests are counted as errors.
A found just means there could be an account not that there is

## Requirements

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Disclaimer

This tool is intended for educational purposes and legitimate OSINT research.

Only use RepoRecon against accounts and information that you are authorised to investigate.
