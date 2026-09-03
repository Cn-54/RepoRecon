import subprocess
import sys
import tempfile
from pathlib import Path

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

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py <repository-url>")
        return

    target = sys.argv[1]

    audit_repo(target)



if __name__ == "__main__":
    main()