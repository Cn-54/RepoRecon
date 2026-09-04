from pathlib import Path
import importlib
from tools.utils._clear_terminal import clear


TOOLS_DIR = Path(__file__).parent / "tools"

PAGES = {
    "repo": "REPOSITORY TOOLS",
    "user": "USER TOOLS",
    "misc": "MISC"
}




# gets a list of tools in the given category
def get_tools(category):
    tool_dir = TOOLS_DIR / category
    tools = []

    if not tool_dir.exists():
        return tools

    for file in sorted(tool_dir.glob("*.py")):

        # skip helper modules
        if file.name.startswith("_"):
            continue

        module_name = f"tools.{category}.{file.stem}"

        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f" [!] Failed to load {file.name}: {e}")
            continue

        # Only include files that have a run() function
        if hasattr(module, "run"):
            tools.append((file.stem, module))

    return tools

# formats the file name into the tool name 
def format_name(filename):
    return filename.replace("_", " ").title()

# shows the current page
def show_page(category):
    clear()
    tools = get_tools(category)

    print("\n" + "=" * 50)
    print(" " * 18 + "REPO-RECON")
    print(" " * 13 + PAGES[category])
    print("=" * 50)

    if not tools:
        print("\nNo tools available.")

    else:
        for number, (name, _) in enumerate(tools, 1):
            print(f"{number}. {format_name(name)}")

    print("\n" + "-" * 50)
    print("[N] Next Page    [P] Previous Page    [Q] Quit")
    print("=" * 50)

    return tools

def run_menu():
    pages = list(PAGES.keys())
    current_page = 0

    while True:
        category = pages[current_page]
        tools = show_page(category)

        choice = input("Select an option: ").strip().lower()

        # Quit
        if choice == "q":
            print("\nGoodbye.")
            break

        # Next page
        elif choice == "n":
            current_page = (current_page + 1) % len(pages)

        # Previous page
        elif choice == "p":
            current_page = (current_page - 1) % len(pages)

        # Tool selection
        elif choice.isdigit():

            number = int(choice)

            if 1 <= number <= len(tools):
                _, module = tools[number - 1]

                try:
                    module.run()
                except KeyboardInterrupt:
                    print("\n\n[!] Tool interrupted.")
                except Exception as e:
                    print(f"\n[!] Tool error: {e}")

                input("\nPress Enter to continue...")

            else:
                print("[!] Invalid option.")

        else:
            print("[!] Invalid option.")


if __name__ == "__main__":
    run_menu()