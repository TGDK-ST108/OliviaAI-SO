import networkx as nx
import matplotlib.pyplot as plt

class TerroristPredictionSystem:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, name, activity_score):
        """Add a suspect or cell with an activity score."""
        self.graph.add_node(name, activity_score=activity_score)

    def add_connection(self, person1, person2, strength):
        """Add a connection between two nodes."""
        self.graph.add_edge(person1, person2, strength=strength)

    def predict_threat(self):
        """Identify clusters and assess threat levels."""
        clusters = list(nx.connected_components(self.graph))
        predictions = {}
        for cluster in clusters:
            threat_score = sum(self.graph.nodes[node]["activity_score"] for node in cluster)
            predictions[frozenset(cluster)] = threat_score
        return predictions

    def visualize_network(self):
        """Visualize the network graph."""
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color="red", node_size=700, font_size=10)
        plt.title("Terrorist Cell Network")
        plt.show()

# Example usage
system = TerroristPredictionSystem()
system.add_node("Suspect A", activity_score=7)
system.add_node("Suspect B", activity_score=8)
system.add_node("Cell Leader", activity_score=10)
system.add_connection("Suspect A", "Suspect B", strength=5)
system.add_connection("Suspect B", "Cell Leader", strength=8)

# Predict threats and visualize
threats = system.predict_threat()
print("Predicted Threat Levels:", threats)
system.visualize_network()