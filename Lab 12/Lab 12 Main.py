from collections import deque, defaultdict
import matplotlib.pyplot as plt
import networkx as nx

# Definicja pojemności krawędzi
capacity = {
    's': {'a': 4, 'c': 10},
    'a': {'b': 3, 'd': 6},
    'b': {'d': 5, 't': 10},
    'c': {'d': 9},
    'd': {'t': 7, 'c': 5},
    't': {}
}

# Pozycje do rysowania grafu
pos = {
    's': (0, 1),
    'a': (1, 2),
    'b': (3, 2.2),
    'c': (1, 0),
    'd': (2.3, 1),
    't': (4, 1)
}

# BFS szukający ścieżki powiększającej
def bfs(capacity, flow, source, sink, parent):
    visited = set([source])
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for v in capacity[u]:
            residual = capacity[u][v] - flow[u][v]
            if v not in visited and residual > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False

# Funkcja do rysowania grafu
def draw_graph(capacity, flow, pos, augmenting_path=None, pause_time=3):
    G = nx.DiGraph()
    edge_colors = []

    for u in capacity:
        for v in capacity[u]:
            cap = capacity[u][v]
            f = flow[u][v]
            G.add_edge(u, v, label=f'{f}/{cap}')
            if augmenting_path and (u, v) in zip(augmenting_path, augmenting_path[1:]):
                edge_colors.append('red')
            else:
                edge_colors.append('black')

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, arrowsize=25)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True, width=2)

    if augmenting_path:
        plt.title(f"Ścieżka powiększająca: {' → '.join(augmenting_path)}")
    else:
        plt.title("Końcowy przepływ")
    plt.show(block=False)
    plt.pause(pause_time)
    plt.close()

# Odtwarzanie ścieżki z BFS
def get_path(parent, source, sink):
    path = []
    v = sink
    while v != source:
        path.append(v)
        v = parent[v]
    path.append(source)
    return list(reversed(path))

# Główna funkcja algorytmu Edmondsa-Karpa
def edmonds_karp(capacity, source, sink, pos):
    flow = defaultdict(lambda: defaultdict(int))
    max_flow = 0
    parent = {}

    while bfs(capacity, flow, source, sink, parent):
        path = get_path(parent, source, sink)
        path_flow = min(capacity[u][v] - flow[u][v] for u, v in zip(path, path[1:]))

        for u, v in zip(path, path[1:]):
            flow[u][v] += path_flow
            flow[v][u] -= path_flow  # Przepływ odwrotny

        max_flow += path_flow
        draw_graph(capacity, flow, pos, augmenting_path=path)
        parent = {}

    return max_flow, flow

# Główne wywołanie
if __name__ == "__main__":
    print("Wyznaczanie maksymalnego przepływu...")
    maxflow, flow_result = edmonds_karp(capacity, 's', 't', pos)
    print("Maksymalny przepływ:", maxflow)
    draw_graph(capacity, flow_result, pos, augmenting_path=None, pause_time=5)