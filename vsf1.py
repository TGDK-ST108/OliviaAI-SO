import matplotlib.pyplot as plt

def visualize_scatter_flow(scatter_vectors, meeting_areas):
    """Visualize scatter flow with vectors and meeting areas."""
    plt.figure(figsize=(10, 8))
    
    # Plot meeting areas
    for area in meeting_areas:
        plt.scatter(area["coordinates"][0], area["coordinates"][1], c="red", label="Meeting Area")
    
    # Plot scatter vectors
    for vector in scatter_vectors:
        start = [0, 0]  # Assuming origin at (0, 0)
        end = vector["direction"] * 5  # Scale for visualization
        plt.quiver(
            start[0], start[1], end[0], end[1],
            angles="xy", scale_units="xy", scale=1, color="blue", alpha=0.6
        )
    
    plt.title("Scatter Flow Processing with Meeting Areas")
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")
    plt.grid(True)
    plt.legend(["Meeting Area", "Flow Vector"])
    plt.show()