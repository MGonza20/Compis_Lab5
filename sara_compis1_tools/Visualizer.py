
import networkx as nx
from graphviz import Digraph

class Visualizer:
    def __init__(self):
        pass

    def draw_mega_afd(self, afd):
        G = nx.MultiDiGraph()
        for state in afd:
            node_attrs = {'shape': 'circle'}
            if state.start:
                node_attrs.update({'color': 'green', 'style': 'filled'})
            if state.accepting:
                node_attrs.update({'peripheries': '2'})
            G.add_node(str(state.name), **node_attrs)

            for transition, final_dest in state.transitions.items():
                G.add_node(str(final_dest))
                
                if ord(transition) in [el for el in range(0, 35)]:
                    transition = str(ord(transition))

                    if len(transition) == 1:
                        transition = '00' + transition
                    elif len(transition) == 2:
                        transition = '0' + transition

                

                G.add_edge(str(state.name), str(final_dest), label=transition, dir='forward')    

        dot = Digraph()
        for u, v, data in G.edges(data=True):
            dot.edge(u, v, label=data['label'], dir=data['dir'])
        for node in G.nodes:
            attrs = G.nodes[node]
            dot.node(node, **attrs)
        dot.render('mega/megaautomata', format='png')