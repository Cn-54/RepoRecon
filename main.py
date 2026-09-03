import sys

from tools.repo_audit import audit_repo
from tools.username_search import reverse_name_search


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