import json
import networkx as nx
import matplotlib.pyplot as plt
import time

#Automat skończony
class AmtSkon:
    def __init__(self, zb_stnw, alfbt, fun_prz, stn_p, zb_stnw_ak):
        self.states = zb_stnw
        self.alphabet = alfbt
        self.transitions = fun_prz
        self.start_state = stn_p
        self.current_state = stn_p
        self.accepting_states = zb_stnw_ak

    def start(self, input_string):
        self.current_state = self.start_state
        print(f"Stan początkowy: {self.current_state}")
        for symbol in input_string:
            if symbol not in self.alphabet:
                print(f"Nieznany symbol: {symbol}")
                print("Język nierozpoznany\n")
                return False
            self.current_state = self.transitions[self.current_state][symbol]
            print(f"Przejście do: {self.current_state}")
        if self.current_state in self.accepting_states:
            print("Język rozpoznany\n")
            return True
        else:
            print("Język nierozponany\n")
            return False


def visualize(automat, input_string):
    G = nx.DiGraph()
    for state, transitions in automat.transitions.items():
        for symbol, next_state in transitions.items():
            G.add_edge(state, next_state, label=symbol)

    pos = nx.spring_layout(G)
    labels = {edge: G.edges[edge]['label'] for edge in G.edges}

    def draw_graph(current_state):
        plt.clf()
        nx.draw(G, pos, with_labels=True,
                node_color=['lightgreen' if state in automat.accepting_states else 'lightblue' for state in G.nodes],
                edge_color='gray', node_size=2000, font_size=12)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx_nodes(G, pos, nodelist=[current_state], node_color='red', node_size=2000)
        plt.pause(1)

    plt.figure(figsize=(8, 6))
    current_state = automat.start_state
    draw_graph(current_state)

    for symbol in input_string:
        time.sleep(1)
        if symbol in automat.alphabet:
            current_state = automat.transitions[current_state][symbol]
            draw_graph(current_state)
    plt.show()


#Zad 1
#Ustawienia do zadania 1
states_1 = {"q0", "q1", "q2", "q3"}
alphabet_1 = {"0", "1"}
transitions_1 = {
    "q0": {"0": "q1", "1": "q0"},
    "q1": {"0": "q3", "1": "q2"},
    "q2": {"0": "q2", "1": "q0"},
    "q3": {"0": "q2", "1": "q2"}
}
start_state_1 = "q0"
accepting_states_1 = {"q3"}

automat_1 = AmtSkon(states_1, alphabet_1, transitions_1, start_state_1, accepting_states_1)

listy_1 = ["001100", "010100", "10110"]
for i in listy_1:
    print(f"\nPrzebieg maszyny dla listy '{i}'")
    automat_1.start(i)

#Zad 2
#Ustawienia do zadania 2
states_2 = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
alphabet_2 = {"a", "b", "c"}
transitions_2 = {
    "q0": {"a": "q2", "b": "q2", "c": "q2"},
    "q1": {"a": "q4", "b": "q0", "c": "q3"},
    "q2": {"a": "q1", "b": "q1", "c": "q6"},
    "q3": {"a": "q3", "b": "q3", "c": "q3"},
    "q4": {"a": "q0", "b": "q5", "c": "q5"},
    "q5": {"a": "q4", "b": "q4", "c": "q4"},
    "q6": {"a": "q3", "b": "q3", "c": "q3"},
}
start_state_2 = "q0"
accepting_states_2 = {"q3", "q4", "q5"}

automat_2 = AmtSkon(states_2, alphabet_2, transitions_2, start_state_2, accepting_states_2)

listy_2 = ["aba", "cba", "abcbc"]
for i in listy_2:
    print(f"\nPrzebieg maszyny dla listy '{i}'")
    automat_2.start(i)
    visualize(automat_2, i)

#Zad 3
#Ustawienia do zadania 3
states_3 = {"q0", "q1", "q2", "q3"}
alphabet_3 = {"a","0", "1"}
transitions_3 = {
    "q0": {"a": "q1", "0": "q3", "1": "q3"},
    "q1": {"a": "q2", "0": "q1", "1": "q1"},
    "q2": {"a": "q3", "0": "q2", "1": "q2"},
    "q3": {"a": "q3", "0": "q3", "1": "q3"},
}
start_state_3 = "q0"
accepting_states_3 = {"q2"}

automat_3 = AmtSkon(states_3, alphabet_3, transitions_3, start_state_3, accepting_states_3)
listy_3 = ["aa1", "a011a10", "a0110", "10011"]

for i in listy_3:
    print(f"\nPrzebieg maszyny dla listy '{i}'")
    automat_3.start(i)

# Zad 4
#Ustawienia do zadania 4
states_4 = {"q0", "q1", "q2", "q3"}
alphabet_4 = {"a", "b", "c", "d"}
transitions_4 = {
    "q0": {"a": "q0", "b": "q1", "c": "q3", "d": "q3"},
    "q1": {"a": "q3", "b": "q3", "c": "q2", "d": "q3"},
    "q2": {"a": "q3", "b": "q3", "c": "q3", "d": "q2"},
    "q3": {"a": "q3", "b": "q3", "c": "q3", "d": "q3"}
}
start_state_4 = "q0"
accepting_states_4 = {"q2"}

automat_4 = AmtSkon(states_4, alphabet_4, transitions_4, start_state_4, accepting_states_4)
listy_4 = ["bc", "aabcddd", "dddbcaa"]

for i in listy_4:
    print(f"\nPrzebieg maszyny dla listy '{i}'")
    automat_4.start(i)

# Zad 5
#Plik na bazie zadania 4
with open('zad4.json', 'r') as file:
    data1 = json.load(file)

#Plik zewnętrzny
with open('data1.json', 'r') as file:
    data2 = json.load(file)

data_packs = [data1, data2]

for data in data_packs:
    states_5 = set(data["states"])
    alphabet_5 = set(data["alphabet"])
    transitions_5 = data["transitions"]
    start_state_5 = data["start_state"]
    accepting_states_5 = set(data["accepting_states"])

    automat_5 = AmtSkon(states_5, alphabet_5, transitions_5, start_state_5, accepting_states_5)
    listy_5 = data["test_inputs"]
    for i in listy_5:
        print(f"\nPrzebieg maszyny dla listy '{i}'")
        automat_5.start(i)