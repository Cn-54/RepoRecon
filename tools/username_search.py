import requests

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

        return exists, url

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

    found = False

    for site in sites:
        exists, url = check_site(site, username)

        if exists:
            print(f"  {url}", flush=True)
            found = True

    if not found:
        print("  No accounts found.")

    print()