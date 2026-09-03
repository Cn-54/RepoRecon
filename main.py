import subprocess
import sys
import tempfile
from pathlib import Path


SITES_FILE = "sites.txt"

def audit_repo(repo_url):
    authors = {}

    with tempfile.TemporaryDirectory() as tmp:
        repo_path = Path(tmp) / "repo"

        print("\nCloning repository...")

        # clone repo into the temp dir
        subprocess.run(
                ["git", "clone", "--quiet", repo_url, str(repo_path)],
                check=True
            )

        # runs git log and grabs the results
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repo_path),
                "log",
                "--format=%H|%an|%ae"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        # splits the commit up into an array
        commits = result.stdout.strip().splitlines()

        # goes through each commit and grabs unique emails and names and the number of commits
        for commit in commits:
            commit_hash, name, email = commit.split("|", 2)

            if email not in authors:
                authors[email] = {
                    "name": name,
                    "commits": 0
                }

            authors[email]["commits"] += 1

        # TemporaryDirectory automatically deletes
        # the cloned repository here.


        print("\n" + "=" * 50)
        print("REPO DETAILS")
        print("=" * 50)

        print(f"Repository: {repo_url}")
        print(f"Total commits: {len(commits)}")

        print("\nAuthors:")
        print("-" * 50)

        for email, data in authors.items():
            name = data["name"]
            commit_count = data["commits"]

            print(f"\nName: {name}")
            print(f"Email: {email}" , end="")

            if email.endswith("@users.noreply.github.com"):
                print()
            else:
                print(" [!] personal email")

            print(f"Commit amount: {commit_count}")

        # Search every unique author name
        unique_names = set(
            data["name"]
            for data in authors.values()
        )

        print("\n")


def load_sites():
    sites = []

    try:
        with open(SITES_FILE, "r") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                sites.append(line)

    except FileNotFoundError:
        print(f"\n[!] {SITES_FILE} not found.")
        return []

    return sites


def check_site(site, username):
    username = username.replace(" ", "")
    url = site.format(username)

    try:
        response = requests.get(
            url,
            timeout=5,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        )

        if response.status_code != 200:
            exists = False

        else:
            # Check whether username appears on page
            exists = username.lower() in response.text.lower()

        return exists, url

    except requests.RequestException:
        return False, url

def reverse_name_search(target):
    sites = load_sites()

    if not sites:
        print(f"no sites in {SITES_FILE}")

    print("=" * 50)
    print("REVERSE USERNAME SEARCH")
    print("=" * 50)

    print(f"Name: {username}")
    print()

    found = []

    for site in sites:
        exists, url = check_site(site, username)

        if exists:
            found.append(url)
    if not found:
        print("  No accounts found.")

        print()

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python main.py repo <repository-url>")
        print("  python main.py username <username>")
        print("  python main.py dual <repository-url>")
        return

    command = sys.argv[1]
    target = sys.argv[2]

    if command == "repo":
        audit_repo(target)
    elif command == "username":
        reverse_name_search(target)
    elif command == "dual":
        audit_repo(target)
        reverse_name_search(target)
    else:
        print("command not recognised!")



if __name__ == "__main__":
    main()