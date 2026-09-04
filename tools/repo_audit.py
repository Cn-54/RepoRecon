import subprocess
import tempfile
from pathlib import Path

def audit_repo(repo_url):
    authors = {}

    with tempfile.TemporaryDirectory() as tmp:
        repo_path = Path(tmp) / "repo"

        print("\nCloning repository...")

        # clone repo into the temp dir
        try:
            subprocess.run(
                ["git", "clone", "--quiet", repo_url, str(repo_path)],
                check=True
            )
        except subprocess.CalledProcessError:
            print("[!] Failed to clone repository.")
            return {}

        # runs git log and grabs the results
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repo_path),
                "log",
                "--format=%H|%an|%ae|%aI"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        # splits the commit up into an array
        commits = result.stdout.strip().splitlines()

        # goes through each commit and grabs unique emails, names,
        # commit count, first commit and last commit
        for commit in commits:

            commit_hash, name, email, date = commit.split("|", 3)

            if email not in authors:
                authors[email] = {
                    "name": name,
                    "commits": 0,
                    "first_commit": date,
                    "last_commit": date
                }

            authors[email]["commits"] += 1

            # Update first and last commit dates
            if date < authors[email]["first_commit"]:
                authors[email]["first_commit"] = date

            if date > authors[email]["last_commit"]:
                authors[email]["last_commit"] = date

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
                print(" [!] Non github email")

            print(f"Commit amount: {commit_count}")
            print(f"First commit: {data["first_commit"]}")
            print(f"Last commit: {data["last_commit"]}")
        

        print("\nAuthor Commit percentages:")
        print("-" * 50)

        for email, data in authors.items():
            name = data["name"]
            commit_count = data["commits"]
            percentage = commit_count / len(commits) * 100

            print(f"\nName: {name}")
            print(f"Commits: {commit_count}")
            print(f"Percentage: {percentage:.2f}%")

        # Search every unique author name
        unique_names = set(
            data["name"]
            for data in authors.values()
        )

        print("\n")
        return authors
