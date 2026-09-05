import networkx as nx
from graphviz import Graph
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
        print(f"[!] Request error for {username}: {error}")
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


def get_connections(username):

    connections = set()

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

    if followers.status_code == 200:
        for user in followers.json():
            connections.add(user["login"])
    else:
        print(
            f"[!] Followers API error for {username}: "
            f"{followers.status_code}"
        )

    if following.status_code == 200:
        for user in following.json():
            connections.add(user["login"])
    else:
        print(
            f"[!] Following API error for {username}: "
            f"{following.status_code}"
        )

    return list(connections)


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

    queue.append((target, 0))

    while queue:

        username, depth = queue.popleft()

        if username in visited:
            continue

        visited.add(username)

        print(
            f"[*] Processing {username} "
            f"(depth {depth})"
        )

        if not add_user_to_graph(graph, username):
            continue

        if depth >= max_depth:
            continue

        connections = get_connections(username)

        for connection in connections:
            graph.add_edge(
                username,
                connection
            )

        for connection in connections[:max_connections]:

            if connection not in visited:

                queue.append(
                    (connection, depth + 1)
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

    dot = Graph(
        name=f"{username}-connections",
        format="png"
    )

    output_dir = Path("outputs")

    output_dir.mkdir(
        exist_ok=True
    )

    for node, data in graph.nodes(data=True):

        label = (
            f"{node}\n"
            f"Email: {data['email']}\n"
            f"Public repos: {data['public_repos']}\n"
            f"Followers: {data['followers']}\n"
            f"Following: {data['following']}"
        )

        dot.node(
            node,
            label=label,
            shape="box"
        )

    for user_a, user_b in graph.edges():

        dot.edge(
            user_a,
            user_b
        )

    output_path = output_dir / f"{username}-connections"

    dot.render(
        filename=str(output_path),
        cleanup=True
    )

    return f"{output_path}.png"


def run():

    username = input(
        "GitHub username: "
    ).strip()

    depth = int(
        input("Maximum depth: ")
    )

    connections = int(
        input(
            "Maximum connections per account: "
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
        f"[+] Relationships: "
        f"{graph.number_of_edges()}"
    )