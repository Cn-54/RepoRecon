import networkx as nx

from graphviz import Graph

from pathlib import Path

from collections import deque

import requests

from dotenv import load_dotenv

import os


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_API_TOKEN")


def get_user_data(username):

    url = f"https://api.github.com/users/{username}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    if response.status_code != 200:
        print(f"[!] GitHub API error: {response.status_code}")
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


def get_mutuals(username):

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    followers_url = f"https://api.github.com/users/{username}/followers"
    following_url = f"https://api.github.com/users/{username}/following"

    followers = requests.get(
        followers_url,
        headers=headers,
        params={"per_page": 100},
        timeout=10
    )

    following = requests.get(
        following_url,
        headers=headers,
        params={"per_page": 100},
        timeout=10
    )

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


def traverse_graph(graph, target, max_depth, max_connections):

    queue = deque()

    visited = set()

    queue.append((target, 0))

    while queue:

        username, depth = queue.popleft()

        if username in visited:
            continue

        visited.add(username)

        user_data = get_user_data(username)

        if user_data is None:
            continue

        graph.add_node(
            username,
            email=user_data["email"],
            links=user_data["links"],
            public_repos=user_data["public_repos"],
            followers=user_data["followers"],
            following=user_data["following"]
        )

        if depth >= max_depth:
            continue

        mutuals = get_mutuals(username)

        mutuals = mutuals[:max_connections]

        for mutual in mutuals:

            graph.add_edge(
                username,
                mutual
            )

            if mutual not in visited:

                queue.append(
                    (mutual, depth + 1)
                )


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
        name=f"{username}-mutuals",
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

    dot.render(
        filename=str(
            output_dir / f"{username}-mutuals"
        ),
        cleanup=True
    )


def run():

    username = input(
        "GitHub username: "
    )

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

    render_graph(
        graph,
        username
    )

    print(
        f"Graph saved to outputs/{username}-mutuals.png"
    )