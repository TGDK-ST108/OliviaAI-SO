def duomotor_control(angle_x, angle_y, zoom_level):
    """Simulate duomotor control for adjusting scope visualization."""
    transformation_matrix = np.array([
        [np.cos(np.radians(angle_x)), -np.sin(np.radians(angle_y))],
        [np.sin(np.radians(angle_x)), np.cos(np.radians(angle_y))]
    ])
    zoom_factor = zoom_level
    return transformation_matrix, zoom_factor