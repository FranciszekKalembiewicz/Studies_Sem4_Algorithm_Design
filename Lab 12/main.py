import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from collections import deque

INPUT_FILE = "Lab11/graph.txt"
SOURCE = "s"
SINK = "t"


def read_graph(filename):
    edges = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            u, v, cap = line.split()
            edges.append((u, v, int(cap)))
    if not edges:
        raise ValueError("Brak krawędzi w pliku.")
    return edges


def build_network(edges):
    G = nx.DiGraph()
    for u, v, cap in edges:
        if G.has_edge(u, v):
            G[u][v]["capacity"] += cap
        else:
            G.add_edge(u, v, capacity=cap, flow=0)
            if not G.has_edge(v, u):
                G.add_edge(v, u, capacity=0, flow=0)
    return G


def bfs_path(G, s, t, parent):
    for v in G:
        parent[v] = None
    visited = {s}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in G.successors(u):
            data = G[u][v]
            if data["capacity"] - data["flow"] > 0 and v not in visited:
                visited.add(v)
                parent[v] = u
                if v == t:
                    bottleneck = float("inf")
                    w = t
                    while w != s:
                        u2 = parent[w]
                        bottleneck = min(
                            bottleneck, G[u2][w]["capacity"] - G[u2][w]["flow"])
                        w = u2
                    return bottleneck
                q.append(v)
    return 0


def collect_states(G0, s, t):
    G = G0.copy()
    parent = {v: None for v in G}
    states = []
    max_flow = 0
    itr = 0

    while True:
        itr += 1
        b = bfs_path(G, s, t, parent)
        if b == 0:
            break

        flow_before = sum(G[s][v]["flow"] for v in G.successors(s))
        title_pre = f"Iter {itr}: bottleneck={b}, flow przed={flow_before}"
        Gpre = nx.DiGraph()
        for u, v, d in G.edges(data=True):
            Gpre.add_edge(u, v, capacity=d["capacity"], flow=d["flow"])
        states.append((Gpre, title_pre))

        w = t
        while w != s:
            u2 = parent[w]
            G[u2][w]["flow"] += b
            G[w][u2]["flow"] -= b
            w = u2
        max_flow += b

        flow_after = sum(G[s][v]["flow"] for v in G.successors(s))
        title_post = f"Iter {itr}: flow po={flow_after}"
        Gpost = nx.DiGraph()
        for u, v, d in G.edges(data=True):
            Gpost.add_edge(u, v, capacity=d["capacity"], flow=d["flow"])
        states.append((Gpost, title_post))

    title_fin = f"KONIEC: max flow={max_flow}"
    Gfin = nx.DiGraph()
    for u, v, d in G.edges(data=True):
        Gfin.add_edge(u, v, capacity=d["capacity"], flow=d["flow"])
    states.append((Gfin, title_fin))
    return states, max_flow


def draw_state(ax, G, pos, title):
    ax.clear()
    edge_colors = []
    edge_widths = []
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        f, c = d["flow"], d["capacity"]
        if c == 0:
            continue
        edge_labels[(u, v)] = f"{f}/{c}"
        if f == 0:
            edge_colors.append("gray")
            edge_widths.append(1)
        elif f < c:
            edge_colors.append("blue")
            edge_widths.append(2)
        else:
            edge_colors.append("red")
            edge_widths.append(3)

    nx.draw_networkx_nodes(G, pos, node_color="lightyellow",
                           edgecolors="black", node_size=800, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20,
                           edge_color=edge_colors, width=edge_widths, connectionstyle="arc3,rad=0.1", ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10, ax=ax)
    ax.set_title(title, fontsize=10)
    ax.axis("off")
    plt.tight_layout()


class Visualizer:
    def __init__(self, states, pos):
        self.states = states
        self.pos = pos
        self.i = 0
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        plt.subplots_adjust(bottom=0.2)
        G0, title0 = states[0]
        draw_state(self.ax, G0, pos, title0)
        axb = plt.axes([0.0, 0.05, 0.2, 0.075])
        self.btn = Button(axb, "Next")
        self.btn.on_clicked(self.next)
        plt.show()

    def next(self, event):
        if self.i + 1 >= len(self.states):
            self.btn.label.set_text("Done")
            self.btn.disconnect_events()
            return
        self.i += 1
        Gsnap, title = self.states[self.i]
        draw_state(self.ax, Gsnap, self.pos, title)
        self.fig.canvas.draw_idle()


def main():
    try:
        edges = read_graph(INPUT_FILE)
    except Exception as e:
        print("[BŁĄD]", e)
        return

    G0 = build_network(edges)
    if SOURCE not in G0 or SINK not in G0:
        print(f"[BŁĄD] Brak '{SOURCE}' lub '{SINK}'")
        return

    states, mf = collect_states(G0, SOURCE, SINK)
    print(f"Zebrano {len(states)} stanów, max flow={mf}")

    pos = {
        "s": (0, 2),
        "a": (1, 3),
        "b": (2, 3),
        "c": (1, 1),
        "d": (2, 1),
        "t": (3, 2)
    }

    Visualizer(states, pos)


if __name__ == "__main__":
    main()
