import networkx as nx
from graphviz import Graph
from pathlib import Path
from collections import deque
import requests

def get_user_data(username):

    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    if response.status_code != 200:
        print(f" [!] GitHub API error: {response.status_code}")
        print(response.text)
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

    followers_url = f"https://api.github.com/users/{username}/followers"
    following_url = f"https://api.github.com/users/{username}/following"

    followers = requests.get(
        followers_url,
        params={"per_page": 100}
    )

    following = requests.get(
        following_url,
        params={"per_page": 100}
    )

    if followers.status_code == 200:
        for user in followers.json():
            connections.add(user["login"])

    if following.status_code == 200:
        for user in following.json():
            connections.add(user["login"])

    return list(connections)


def traverse_graph(graph, target, max_depth, max_connections):

    queue = deque()
    visited = set()

    # target starts at depth 0
    queue.append((target, 0))

    while queue:

        username, depth = queue.popleft()

        # Dont process the same user twice
        if username in visited:
            continue

        visited.add(username)

        # get information about this user
        user_data = get_user_data(username)

        # add the user to the graph
        graph.add_node(
            username,
            email=user_data["email"],
            links=user_data["links"],
            public_repos=user_data["public_repos"],
            followers=user_data["followers"],
            following=user_data["following"]
        )

        # dont expand users at the maximum depth
        if depth >= max_depth:
            continue

        # get this users connections
        connections = get_connections(username)

        # limit how many connections we follow
        connections = connections[:max_connections]

        for connection in connections:

            # add the connection to the graph
            graph.add_edge(username, connection)

            # add the connection to the queue
            if connection not in visited:
                queue.append((connection, depth + 1))


def build_graph(target, max_depth, max_connections):

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
        name=username,
        format="png"
    )

    # create output directory
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # add nodes
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

    # add relationships
    for user_a, user_b in graph.edges():

        dot.edge(
            user_a,
            user_b
        )

    # render to outputs/<username>.png
    dot.render(
        filename=str(output_dir / username),
        cleanup=True
    )


def run():

    username = input("GitHub username: ")

    depth = int(input("Maximum depth: "))

    connections = int(input("Maximum connections per account: "))

    graph = build_graph(
        username,
        depth,
        connections
    )

    render_graph(
        graph,
        username
    )

    print(
        f"Graph saved to outputs/{username}.png"
    )

