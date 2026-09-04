import requests
from tools.utils._clear_terminal import clear

SITES_FILE = "sites.txt"

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

        return exists, url, response.status_code
    except requests.RequestException:
        return False, url, None

    except requests.RequestException:
        return False, url

def reverse_name_search(username):
    sites = load_sites()

    if not sites:
        print(f"no sites in {SITES_FILE}")
        return

    print("=" * 50)
    print("REVERSE USERNAME SEARCH")
    print("=" * 50)
    print(f"Name: {username}")
    print()

    found = 0
    not_found = 0
    error = 0

    for site in sites:
        exists, url, code = check_site(site, username)

        if exists:
            print(f"  [+] {url}", flush=True)
            found += 1
        elif code == 404:
            not_found += 1
        else:
            error += 1

    print("\n" + "-" * 50)
    print("Search complete")
    print("-" * 50)
    print(f"Sites checked : {len(sites)}")
    print(f"Accounts found: {found}")
    print(f"Not found     : {not_found}")
    print(f"Errors        : {error}")

    print()



def run():
    username = input("\nEnter username: ").strip()

    if not username:
        print("[!] No username provided.")
        return

    clear()
    reverse_name_search(username)