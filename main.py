import os

from tools.repo_audit import audit_repo
from tools.username_search import reverse_name_search

def clear():
    # 'cls' for Windows, 'clear' for macOS/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    clear()
    print("\n" + "=" * 50)
    print("                 REPO-RECON")
    print("=" * 50)

    print("1. Repository Audit")
    print("2. Username Search")
    print("3. Repository + Username Search")
    print("4. Exit")

    print("=" * 50)


def main():

    while True:

        display_menu()

        choice = input("Select an option: ").strip()

        if choice == "1":

            repo_url = input("\nEnter repository URL: ").strip()

            if repo_url:
                audit_repo(repo_url)

        elif choice == "2":

            username = input("\nEnter username: ").strip()

            if username:
                reverse_name_search(username)

        elif choice == "3":

            repo_url = input("\nEnter repository URL: ").strip()

            if repo_url:
                authors = audit_repo(repo_url)

                # Get unique names from repository
                names = {
                    data["name"]
                    for data in authors.values()
                }

                for name in names:
                    reverse_name_search(name)

        elif choice == "4":

            print("\nExiting...")
            break

        else:

            print("\n[!] Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()