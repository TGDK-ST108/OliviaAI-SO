import numpy as np

def generate_scatter_vectors(zones):
    """Generate directional vectors for scatter flow processing."""
    scatter_vectors = []
    for zone in zones:
        angle = np.random.uniform(0, 360)  # Random angle in degrees
        vector = {
            "zone_id": zone["ID"],
            "angle": angle,
            "direction": np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))])  # 2D vector
        }
        scatter_vectors.append(vector)
    return scatter_vectors

def map_to_meeting_areas(scatter_vectors, meeting_areas):
    """Map vectors to zonal meeting areas and calculate occlusion."""
    mapped_areas = []
    for vector in scatter_vectors:
        # Determine the closest meeting area
        meeting_area = min(
            meeting_areas,
            key=lambda area: np.linalg.norm(vector["direction"] - np.array(area["coordinates"]))
        )
        mapped_areas.append({"zone_id": vector["zone_id"], "meeting_area": meeting_area})
    return mapped_areas

def apply_occlusion(mapped_areas):
    """Simulate occlusion to control overlap in meeting areas."""
    occluded_data = []
    for area in mapped_areas:
        if area["meeting_area"]["capacity"] > 0:  # Capacity limit for occlusion
            area["meeting_area"]["capacity"] -= 1  # Occupy capacity
            occluded_data.append(area)
    return occluded_data

