import networkx as nx
from pyvis.network import Network
from pathlib import Path
from collections import deque
import requests
from dotenv import load_dotenv
import os


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_user_data(username):
    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
    except requests.RequestException as error:
        print(
            f"[!] Request error for {username}: "
            f"{error}"
        )
        return None

    if response.status_code != 200:
        print(
            f"[!] GitHub API error for {username}: "
            f"{response.status_code}"
        )
        return None

    data = response.json()

    return {
        "username": data["login"],
        "email": data.get("email") or "N/A",
        "links": [data["blog"]] if data.get("blog") else [],
        "public_repos": data["public_repos"],
        "followers": data["followers"],
        "following": data["following"]
    }


def get_mutuals(username):

    followers_url = (
        f"https://api.github.com/users/{username}/followers"
    )

    following_url = (
        f"https://api.github.com/users/{username}/following"
    )

    try:

        followers = requests.get(
            followers_url,
            headers=HEADERS,
            params={"per_page": 100},
            timeout=10
        )

        following = requests.get(
            following_url,
            headers=HEADERS,
            params={"per_page": 100},
            timeout=10
        )

    except requests.RequestException as error:

        print(
            f"[!] Connection request error for "
            f"{username}: {error}"
        )

        return []

    if followers.status_code != 200:

        print(
            f"[!] Followers API error for {username}: "
            f"{followers.status_code}"
        )

        return []

    if following.status_code != 200:

        print(
            f"[!] Following API error for {username}: "
            f"{following.status_code}"
        )

        return []

    follower_names = {
        user["login"]
        for user in followers.json()
    }

    following_names = {
        user["login"]
        for user in following.json()
    }

    mutuals = follower_names & following_names

    return list(mutuals)


def add_user_to_graph(graph, username):

    user_data = get_user_data(username)

    if user_data is None:
        return False

    graph.add_node(
        username,
        email=user_data["email"],
        links=user_data["links"],
        public_repos=user_data["public_repos"],
        followers=user_data["followers"],
        following=user_data["following"]
    )

    return True


def traverse_graph(
    graph,
    target,
    max_depth,
    max_connections
):

    queue = deque()

    visited = set()

    queue.append(
        (target, 0)
    )

    while queue:

        username, depth = queue.popleft()

        if username in visited:
            continue

        visited.add(username)

        print(
            f"[*] Processing {username} "
            f"(depth {depth})"
        )

        if not add_user_to_graph(
            graph,
            username
        ):
            continue

        if depth >= max_depth:
            continue

        mutuals = get_mutuals(username)

        # Add ALL mutual relationships discovered
        # for this account.
        for mutual in mutuals:

            graph.add_edge(
                username,
                mutual
            )

        for mutual in mutuals[:max_connections]:

            if mutual not in visited:

                queue.append(
                    (mutual, depth + 1)
                )


def build_graph(
    target,
    max_depth,
    max_connections
):

    graph = nx.Graph()

    traverse_graph(
        graph,
        target,
        max_depth,
        max_connections
    )

    return graph


def render_graph(graph, username):

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{username}-connections.html"

    net = Network(
        height="900px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=False
    )

    for node, data in graph.nodes(data=True):

        email = data.get("email", "N/A")
        public_repos = data.get("public_repos", "N/A")
        followers = data.get("followers", "N/A")
        following = data.get("following", "N/A")

        title = (
            f"<b>{node}</b><br>"
            f"Email: {email}<br>"
            f"Public repos: {public_repos}<br>"
            f"Followers: {followers}<br>"
            f"Following: {following}"
        )

        net.add_node(
            node,
            label=node,
            title=title,
            shape="box"
        )

    for user_a, user_b in graph.edges():
        net.add_edge(user_a, user_b)

    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "stabilization": {
                "iterations": 1000
            },
            "barnesHut": {
                "gravitationalConstant": -3000,
                "centralGravity": 0.2,
                "springLength": 150,
                "springConstant": 0.04,
                "damping": 0.09
            }
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true
        }
    }
    """)

    net.write_html(
        str(output_file),
        open_browser=False
    )

    print(f"[+] Graph saved to {output_file}")


def run():

    username = input(
        "GitHub username: "
    ).strip()

    depth = int(
        input("Maximum depth: ")
    )

    connections = int(
        input(
            "Maximum mutuals per account: "
        )
    )

    graph = build_graph(
        username,
        depth,
        connections
    )

    output = render_graph(
        graph,
        username
    )

    print(
        f"\n[+] Graph saved to {output}"
    )

    print(
        f"[+] Nodes: {graph.number_of_nodes()}"
    )

    print(
        f"[+] Mutual relationships: "
        f"{graph.number_of_edges()}"
    )