
import logging
import matplotlib.pyplot as plt
import networkx as nx

class SchematicOvercharting:
    def __init__(self):
        self.graph = nx.DiGraph()
        logging.info("SchematicOvercharting initialized.")

    def add_component(self, component: str):
        self.graph.add_node(component)
        logging.info("Added component: %s", component)

    def add_dependency(self, from_component: str, to_component: str):
        self.graph.add_edge(from_component, to_component)
        logging.info("Added dependency from '%s' to '%s'.", from_component, to_component)

    def visualize_schematic(self, filename: str = "schematic.png"):
        logging.info("Visualizing schematic overchart.")
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", arrows=True)
        plt.title("Schematic Overchart")
        plt.savefig(filename)
        plt.close()
        logging.info("Schematic visualization saved as '%s'.", filename)
