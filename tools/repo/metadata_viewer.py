import requests
from tools.utils._clear_terminal import clear

def metadata_viewer(URL):
    repo = URL.rstrip("/").removesuffix(".git")

    if "github.com/" not in repo:
        print("[!] Invalid GitHub repository URL.")
        return {}

    repo = repo.split("github.com/", 1)[1]
    parts = repo.split("/")

    if len(parts) != 2:
        print("[!] Invalid GitHub repository URL.")
        return {}

    owner, repo_name = parts

    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"

    print("\nFetching repository metadata...")

    try:
        response = requests.get(
            api_url,
            headers={
                "Accept": "application/vnd.github+json"
            },
            timeout=10
        )

    except requests.RequestException:
        print("[!] Failed to connect to GitHub.")
        return {}

    if response.status_code == 404:
        print("[!] Repository not found.")
        return {}

    if response.status_code != 200:
        print(f"[!] GitHub API returned status {response.status_code}.")
        return {}

    data = response.json()

    print("\n" + "=" * 50)
    print("REPOSITORY METADATA")
    print("=" * 50)

    print(f"Name: {data['name']}")
    print(f"Owner: {data['owner']['login']}")
    print(f"Description: {data['description'] or 'None'}")
    print(f"Visibility: {data['visibility']}")
    print(f"Default branch: {data['default_branch']}")

    print("\nRepository Statistics:")
    print("-" * 50)

    print(f"Stars: {data['stargazers_count']}")
    print(f"Forks: {data['forks_count']}")
    print(f"Open issues: {data['open_issues_count']}")
    print(f"Watchers: {data['watchers_count']}")

    print("\nRepository Information:")
    print("-" * 50)

    print(f"Language: {data['language'] or 'None'}")
    print(f"License: {data['license']['name'] if data['license'] else 'None'}")
    print(f"Created: {data['created_at']}")
    print(f"Last updated: {data['updated_at']}")
    print(f"Last pushed: {data['pushed_at']}")

    if data["topics"]:
        print("\nTopics:")
        print("-" * 50)

        for topic in data["topics"]:
            print(f"  - {topic}")

    print()

    return data


def run():
    repo_url = input("\nEnter repository URL: ").strip()

    if not repo_url:
        print("[!] No repository URL provided.")
        return

    clear()
    metadata_viewer(repo_url)