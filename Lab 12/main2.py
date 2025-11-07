# -*- coding: utf-8 -*-
"""
Sortowanie topologiczne (Kahn) z wizualizacją krok po kroku.
Wczytuje krawędzie z pliku „u v [liczba]” i ignoruje trzeci token.
Kliknij “Next”, by przejść przez kolejne stany.
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from collections import deque

INPUT_FILE = "Lab11/graph2.txt"


def read_graph_from_file(filename):
    """Wczytaj krawędzie (u v [cokolwiek]) i zbuduj słownik {u: [v,…]}."""
    graph = {}
    all_nodes = set()
    with open(filename, "r") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                raise ValueError(f"Linia {i} w złym formacie: '{line}'")
            u, v = parts[0], parts[1]
            all_nodes.add(u)
            all_nodes.add(v)
            graph.setdefault(u, []).append(v)
            graph.setdefault(v, [])
    return graph, all_nodes


def collect_kahn_states(graph, all_nodes):
    """Zbierz stany algorytmu Kahn’a: (graf, in_degree, opis)."""
    in_degree = {v: 0 for v in all_nodes}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    Q = sorted([v for v in in_degree if in_degree[v] == 0])
    states = []
    topo_order = []

    # początkowy stan
    states.append((
        {u: list(graph[u]) for u in graph},
        in_degree.copy(),
        f"Start: Q={Q}, in_degree={in_degree}"
    ))

    while Q:
        u = Q.pop(0)
        topo_order.append(u)

        # przed usunięciem u
        states.append((
            {x: list(graph[x]) for x in graph},
            in_degree.copy(),
            f"Usuń '{u}' (Q przed = ['{u}']+{Q})"
        ))

        for v in graph[u]:
            in_degree[v] -= 1
            states.append((
                {x: list(graph[x]) for x in graph},
                in_degree.copy(),
                f"Zmniejszam in_degree['{v}'] → {in_degree[v]}"
            ))
            if in_degree[v] == 0:
                Q.append(v)
                Q.sort()
                states.append((
                    {x: list(graph[x]) for x in graph},
                    in_degree.copy(),
                    f"'{v}' do Q → Q={Q}"
                ))

        in_degree[u] = -1  # oznacz usunięty

    if len(topo_order) < len(all_nodes):
        raise Exception("Graf zawiera cykl → brak sortowania.")

    # stan końcowy
    states.append((
        {u: list(graph[u]) for u in graph},
        {v: max(in_degree[v], 0) for v in in_degree},
        f"KONIEC: kolejność={topo_order}"
    ))
    return states, topo_order


def draw_state(ax, graph_snap, in_degree_snap, pos, title):
    """Narysuj graf z kolorowaniem: -1→szary, 0→żółty, >0→niebieski."""
    ax.clear()
    G = nx.DiGraph()
    for u in graph_snap:
        G.add_node(u)
    for u in graph_snap:
        for v in graph_snap[u]:
            G.add_edge(u, v)

    colors = []
    for v in G.nodes():
        d = in_degree_snap.get(v, 0)
        if d == -1:
            colors.append("lightgray")
        elif d == 0:
            colors.append("yellow")
        else:
            colors.append("lightblue")

    labels = {v: f"{v}\n(in={max(in_degree_snap[v], 0)})" for v in G.nodes()}
    nx.draw_networkx_nodes(G, pos, node_color=colors,
                           edgecolors="black", node_size=800, ax=ax)
    nx.draw_networkx_labels(G, pos, labels, font_size=10, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle="->",
                           arrowsize=20, edge_color="gray", ax=ax)

    ax.set_title(title, fontsize=10)
    ax.axis("off")
    plt.tight_layout()


class TopoSortVisualizer:
    """Interaktywne przechodzenie przez stany algorytmu."""

    def __init__(self, states, pos):
        self.states = states
        self.pos = pos
        self.i = 0
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        plt.subplots_adjust(bottom=0.2)
        graph0, in0, title0 = states[0]
        draw_state(self.ax, graph0, in0, pos, title0)

        ax_btn = plt.axes([0, 0.05, 0.3, 0.075])
        self.btn = Button(ax_btn, "Next")
        self.btn.on_clicked(self.next_state)
        plt.show()

    def next_state(self, event):
        if self.i + 1 >= len(self.states):
            self.btn.label.set_text("Done")
            self.btn.disconnect_events()
            return
        self.i += 1
        g_snap, in_snap, title = self.states[self.i]
        draw_state(self.ax, g_snap, in_snap, self.pos, title)
        self.fig.canvas.draw_idle()


def main():
    try:
        graph, all_nodes = read_graph_from_file(INPUT_FILE)
    except Exception as e:
        print(f"[BŁĄD] {e}")
        return

    print(f"Wczytano graf: {len(all_nodes)} węzłów.")
    for u in graph:
        for v in graph[u]:
            print(f"  {u} → {v}")

    print("\nZbieram stany algorytmu...")
    try:
        states, topo_order = collect_kahn_states(graph, all_nodes)
    except Exception as e:
        print(f"[BŁĄD] {e}")
        return

    print(f"Stany: {len(states)}. Kolejność: {topo_order}")

    # stały układ węzłów
    if all_nodes == {"s", "a", "b", "c", "d", "t"}:
        pos = {
            "s": (0, 2),
            "a": (1, 3),
            "b": (2, 3),
            "c": (1, 1),
            "d": (2, 1),
            "t": (3, 2),
        }
    else:
        G_full = nx.DiGraph()
        for u in graph:
            G_full.add_node(u)
            for v in graph[u]:
                G_full.add_edge(u, v)
        pos = nx.spring_layout(G_full, seed=42)

    print("Kliknij 'Next', aby przejść do kolejnego stanu.")
    TopoSortVisualizer(states, pos)


if __name__ == "__main__":
    main()
