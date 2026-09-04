import os

from tools.repo_audit import audit_repo
from tools.username_search import reverse_name_search
from tools.metadata_viewer import metadata_viewer

def clear():
    # 'cls' for Windows, 'clear' for macOS/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    clear()
    print("\n" + "=" * 50)
    print("                 REPO-RECON")
    print("=" * 50)

    print("1. Repository Audit")
    print("2. Repository metadata viewer")
    print("3. Username Search")
    print("4. Repository + Username Search")
    print("5. Exit")

    print("=" * 50)


def main():

    while True:

        display_menu()

        choice = input("Select an option: ").strip()

        if choice == "1":

            repo_url = input("\nEnter repository URL: ").strip()
            
            if repo_url:
                clear()
                audit_repo(repo_url)
            else:
                print("[!] no URL passed")

        elif choice == "2":

            repo_url = input("\nEnter repository URL: ").strip()

            if repo_url:
                clear()
                metadata_viewer(repo_url)
            else:
                print("[!] no URL passed")

        elif choice == "3":

            username = input("\nEnter username: ").strip()

            if username:
                clear()
                reverse_name_search(username)
            else:
                print("[!] no username passed")


        elif choice == "4":

            repo_url = input("\nEnter repository URL: ").strip()

            if repo_url:
                clear()
                authors = audit_repo(repo_url)
                names = {
                    data["name"]
                    for data in authors.values()
                }

                for name in names:
                    reverse_name_search(name)
            else:
                print("[!] no URL passed")

        elif choice == "5":

            print("\nExiting...")
            break

        else:
            print("\n[!] Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()