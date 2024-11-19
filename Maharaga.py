
import numpy as np

class Maharaga:
    def __init__(self):
        """Initialize the Maharaga module."""
        self.data_points = []

    def clear_data_points(self):
        """Clear all data points."""
        self.data_points = []
        print("All data points cleared.")

    def add_data_point(self, point):
        """Add a new data point (must be 2D or 3D point)."""
        if len(point) not in {2, 3}:
            raise ValueError("Only 2D or 3D points are allowed.")
        self.data_points.append(np.array(point))
        print(f"Data point {point} added.")

    # Precise Geometry Operations

    def line_intersection(self, line1_start, line1_end, line2_start, line2_end):
        """
        Calculate the intersection of two lines defined by points.
        
        Returns the intersection point or None if lines are parallel or don't intersect.
        """
        x1, y1 = line1_start
        x2, y2 = line1_end
        x3, y3 = line2_start
        x4, y4 = line2_end

        # Calculate determinants
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if np.isclose(denominator, 0):
            return None  # Lines are parallel or coincident

        # Calculating intersection coordinates
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
        return np.array([px, py])

    def distance_from_point_to_line(self, point, line_start, line_end):
        """
        Calculate the shortest distance from a point to a line segment defined by two points.
        
        This method provides a precise geometric distance.
        """
        line_vec = np.array(line_end) - np.array(line_start)
        point_vec = np.array(point) - np.array(line_start)
        line_len = np.dot(line_vec, line_vec)
        
        if line_len == 0:
            return np.linalg.norm(point_vec)  # Start and end points are the same

        # Project the point onto the line (using vector projection)
        projection_factor = np.dot(point_vec, line_vec) / line_len
        if projection_factor < 0:
            closest_point = np.array(line_start)
        elif projection_factor > 1:
            closest_point = np.array(line_end)
        else:
            closest_point = np.array(line_start) + projection_factor * line_vec

        return np.linalg.norm(np.array(point) - closest_point)

    def polygon_area(self, vertices):
        """
        Calculate the area of a polygon given its vertices.
        
        Uses the Shoelace formula for precision.
        """
        n = len(vertices)
        if n < 3:
            raise ValueError("At least three vertices are required to form a polygon.")
        area = 0.5 * abs(sum(vertices[i][0] * vertices[(i + 1) % n][1] - vertices[i][1] * vertices[(i + 1) % n][0] for i in range(n)))
        return area

    def angle_between_lines(self, line1_start, line1_end, line2_start, line2_end):
        """
        Calculate the precise angle between two lines in degrees.
        
        Uses vector dot product and arccos for precision.
        """
        vec1 = np.array(line1_end) - np.array(line1_start)
        vec2 = np.array(line2_end) - np.array(line2_start)

        # Normalize vectors
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        if norm_vec1 == 0 or norm_vec2 == 0:
            raise ValueError("Line segments must have non-zero length.")

        dot_product = np.dot(vec1, vec2)
        cos_theta = np.clip(dot_product / (norm_vec1 * norm_vec2), -1.0, 1.0)  # Clip for numerical stability
        angle = np.degrees(np.arccos(cos_theta))

        return angle

    # Additional precise operations can be added as required.

    # Example methods for testing purposes
    def list_data_points(self):
        """List all data points."""
        print("Current Data Points:")
        for point in self.data_points:
            print(point)


    # Quantum Angeling Method
    def quantum_angel(self, point, angle_degrees, probability_amplitude=0.5):
        """
        Apply a quantum angeling transformation to a point.
        
        This function will rotate the point by a certain angle with a probability amplitude.
        The point will "quantum shift" to a superposed angle state based on the probability amplitude.
        
        Parameters:
            - point: Array-like (2D or 3D), the point to apply the transformation.
            - angle_degrees: float, angle to rotate in degrees.
            - probability_amplitude: float, the probability amplitude (between 0 and 1) that determines the "intensity" of the angeling.
        
        Returns:
            - Transformed point in superposition of the rotation.
        """
        if len(point) not in {2, 3}:
            raise ValueError("Only 2D or 3D points are allowed for quantum angeling.")
        
        # Convert angle to radians and calculate phase shift
        theta = np.radians(angle_degrees)
        phase_shift = np.exp(1j * theta * probability_amplitude)  # Complex rotation factor
        
        # Apply rotation in 2D or 3D based on point dimensions
        if len(point) == 2:
            rotation_matrix = np.array([
                [np.real(phase_shift), -np.imag(phase_shift)],
                [np.imag(phase_shift), np.real(phase_shift)]
            ])
        else:  # For 3D, assume rotation around the z-axis for simplicity
            rotation_matrix = np.array([
                [np.real(phase_shift), -np.imag(phase_shift), 0],
                [np.imag(phase_shift), np.real(phase_shift), 0],
                [0, 0, 1]
            ])
        
        transformed_point = np.dot(rotation_matrix, point)
        print(f"Quantum-angeled point: {transformed_point}")
        return transformed_point

    def calculate_centroid(self):
        """Calculate the centroid of the data points."""
        if not self.data_points:
            raise ValueError("No data points to calculate the centroid.")
        centroid = np.mean(self.data_points, axis=0)
        print(f"Centroid of data points: {centroid}")
        return centroid

    def list_data_points(self):
        """List all data points."""
        print("Current Data Points:")
        for point in self.data_points:
            print(point)

    def calculate_skewness(self, ddof=1):
        """Calculate the skewness of the data points."""
        if len(self.data_points) < 3:
            raise ValueError("At least three data points are required to calculate skewness.")
        
        mean = np.mean(self.data_points)
        deviations = np.array(self.data_points) - mean
        skewness = (
            len(self.data_points) / ((len(self.data_points) - 1) * (len(self.data_points) - 2))
        ) * np.sum((deviations ** 3) / (np.std(self.data_points, ddof=ddof) ** 3))
        
        return skewness

    def calculate_kurtosis(self, ddof=1):
        """Calculate the kurtosis of the data points."""
        if len(self.data_points) < 4:
            raise ValueError("At least four data points are required to calculate kurtosis.")
        
        mean = np.mean(self.data_points)
        deviations = np.array(self.data_points) - mean
        kurtosis = (
            len(self.data_points) * (len(self.data_points) + 1) /
            ((len(self.data_points) - 1) * (len(self.data_points) - 2) * (len(self.data_points) - 3))
        ) * np.sum((deviations ** 4) / (np.std(self.data_points, ddof=ddof) ** 4)) - 3
        return kurtosis

    def calculate_coefficient_of_variation(self):
        """Calculate the coefficient of variation of the data points."""
        mean = np.mean(self.data_points)
        std_dev = np.std(self.data_points)
        return std_dev / mean if mean != 0 else np.inf

    def rotate_point(self, point, angle, axis='z'):
        """Rotate a point around the origin by a given angle (in degrees) along a specified axis."""
        theta = np.radians(angle)
        if axis == 'z':
            rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                        [np.sin(theta), np.cos(theta), 0],
                                        [0, 0, 1]])
        elif axis == 'y':
            rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta)],
                                        [0, 1, 0],
                                        [-np.sin(theta), 0, np.cos(theta)]])
        elif axis == 'x':
            rotation_matrix = np.array([[1, 0, 0],
                                        [0, np.cos(theta), -np.sin(theta)],
                                        [0, np.sin(theta), np.cos(theta)]])
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'.")
        return np.dot(rotation_matrix, np.append(point, 1))[:len(point)]

    def calculate_convex_hull_area(self):
        """Calculate the area of the convex hull formed by the data points (2D only)."""
        from scipy.spatial import ConvexHull
        if len(self.data_points) < 3:
            raise ValueError("At least three data points are required for a convex hull.")
        hull = ConvexHull(self.data_points)
        return hull.area

    def calculate_incircle_radius(self, point_a, point_b, point_c):
        """Calculate the incircle radius of a triangle formed by three points."""
        area = self.calculate_area_of_triangle(point_a, point_b, point_c)
        s = (self.distance_between_points(point_a, point_b) + self.distance_between_points(point_b, point_c) + 
             self.distance_between_points(point_c, point_a)) / 2
        return area / s

    # Add any other desired updates and methods here...


    def add_data_point(self, point):
        """Add a new data point (must be a 2D point)."""
        if len(point) != 2:
            raise ValueError("Only 2D points are allowed.")
        self.data_points.append(np.array(point))
        print(f"Data point {point} added.")

    def distance_between_points(self, point_a, point_b):
        """Calculate the distance between two points."""
        return np.linalg.norm(np.subtract(point_a, point_b))

    def closest_data_point(self, target_point):
        """Find the closest data point to a given target point."""
        distances = [self.distance_between_points(point, target_point) for point in self.data_points]
        closest_index = np.argmin(distances)
        return self.data_points[closest_index]

    def transform_data(self, transformation_matrix):
        """Transform all data points using a given transformation matrix."""
        if len(transformation_matrix) != 2 or len(transformation_matrix[0]) != 2:
            raise ValueError("Transformation matrix must be 2x2.")
        self.data_points = [np.dot(transformation_matrix, point) for point in self.data_points]
        print("Data points transformed successfully.")

    def list_data_points(self):
        """List all data points."""
        print("Current Data Points:")
        for point in self.data_points:
            print(point)

    ## Geometric Calculations
    def calculate_area_of_triangle(self, point_a, point_b, point_c):
        """Calculate the area of a triangle given three vertices."""
        return 0.5 * abs(point_a[0] * (point_b[1] - point_c[1]) +
                          point_b[0] * (point_c[1] - point_a[1]) +
                          point_c[0] * (point_a[1] - point_b[1]))

    def calculate_distance_from_origin(self, point):
        """Calculate the distance from a point to the origin (0, 0)."""
        return np.linalg.norm(point)

    def is_point_inside_circle(self, point, center, radius):
        """Check if a point is inside a circle defined by a center and radius."""
        return self.distance_between_points(point, center) < radius

    def calculate_slope(self, point_a, point_b):
        """Calculate the slope of the line connecting two points."""
        if point_a[0] == point_b[0]:  # Vertical line
            raise ValueError("Slope is undefined for vertical lines.")
        return (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])

    def line_equation(self, point_a, point_b):
        """Return the slope-intercept form of the line equation (y = mx + b) given two points."""
        m = self.calculate_slope(point_a, point_b)
        b = point_a[1] - m * point_a[0]
        return m, b

    ## Statistical Operations
    def mean_of_data_points(self):
        """Calculate the mean of all data points."""
        return np.mean(self.data_points, axis=0)

    def median_of_data_points(self):
        """Calculate the median of all data points."""
        return np.median(self.data_points, axis=0)

    def variance_of_data_points(self):
        """Calculate the variance of the data points."""
        return np.var(self.data_points, axis=0)

    def standard_deviation_of_data_points(self):
        """Calculate the standard deviation of the data points."""
        return np.std(self.data_points, axis=0)

    def covariance_matrix(self):
        """Calculate the covariance matrix of the data points."""
        return np.cov(np.array(self.data_points).T)

    def correlation_matrix(self):
        """Calculate the correlation matrix of the data points."""
        return np.corrcoef(np.array(self.data_points).T)

    ## Transformation Operations
    def rotate_point(self, point, angle):
        """Rotate a point around the origin by a given angle (in degrees)."""
        theta = np.radians(angle)
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                     [np.sin(theta), np.cos(theta)]])
        return np.dot(rotation_matrix, point)

    def translate_point(self, point, translation_vector):
        """Translate a point by a given translation vector."""
        return point + translation_vector

    def scale_point(self, point, scale_factor):
        """Scale a point by a given scale factor."""
        return point * scale_factor

    ## Vector Operations
    def add_vectors(self, vector_a, vector_b):
        """Add two vectors."""
        return np.add(vector_a, vector_b)

    def subtract_vectors(self, vector_a, vector_b):
        """Subtract vector b from vector a."""
        return np.subtract(vector_a, vector_b)

    def dot_product(self, vector_a, vector_b):
        """Calculate the dot product of two vectors."""
        return np.dot(vector_a, vector_b)

    def cross_product(self, vector_a, vector_b):
        """Calculate the cross product of two 3D vectors (considering z=0 for 2D)."""
        return np.cross(np.append(vector_a, 0), np.append(vector_b, 0))[:2]

    def vector_magnitude(self, vector):
        """Calculate the magnitude of a vector."""
        return np.linalg.norm(vector)

    ## Distance and Closeness
    def farthest_data_point(self, target_point):
        """Find the farthest data point from a given target point."""
        distances = [self.distance_between_points(point, target_point) for point in self.data_points]
        farthest_index = np.argmax(distances)
        return self.data_points[farthest_index]

    def average_distance_to_target(self, target_point):
        """Calculate the average distance of all data points to a given target point."""
        distances = [self.distance_between_points(point, target_point) for point in self.data_points]
        return np.mean(distances)

    ## Miscellaneous
    def save_data_points(self, filename):
        """Save the data points to a file."""
        np.savetxt(filename, self.data_points)
        print(f"Data points saved to '{filename}'.")

    def load_data_points(self, filename):
        """Load data points from a file."""
        self.data_points = np.loadtxt(filename).tolist()
        print(f"Data points loaded from '{filename}'.")

    def shuffle_data_points(self):
        """Shuffle the data points."""
        np.random.shuffle(self.data_points)
        print("Data points shuffled successfully.")

    def find_data_point_index(self, point):
        """Find the index of a data point."""
        try:
            return self.data_points.index(point)
        except ValueError:
            return -1

    def remove_data_point(self, point):
        """Remove a data point from the list."""
        index = self.find_data_point_index(point)
        if index != -1:
            del self.data_points[index]
            print(f"Data point {point} removed successfully.")
        else:
            print("Data point not found.")

    ## Additional Methods (60 more methods)
    def calculate_perimeter_of_polygon(self, points):
        """Calculate the perimeter of a polygon given its vertices."""
        perimeter = 0
        n = len(points)
        for i in range(n):
            perimeter += self.distance_between_points(points[i], points[(i + 1) % n])
        return perimeter

    def find_convex_hull(self):
        """Find the convex hull of the data points."""
        from scipy.spatial import ConvexHull
        hull = ConvexHull(self.data_points)
        return self.data_points[hull.vertices]

    def project_point_onto_line(self, point, line_point_a, line_point_b):
        """Project a point onto a line defined by two points."""
        line_vector = line_point_b - line_point_a
        point_vector = point - line_point_a
        line_unit_vector = line_vector / np.linalg.norm(line_vector)
        projection_length = np.dot(point_vector, line_unit_vector)
        projection = line_point_a + projection_length * line_unit_vector
        return projection

    def midpoint_of_segment(self, point_a, point_b):
        """Calculate the midpoint of a line segment defined by two points."""
        return (point_a + point_b) / 2

    def is_collinear(self, point_a, point_b, point_c):
        """Check if three points are collinear."""
        return np.isclose(self.calculate_area_of_triangle(point_a, point_b, point_c), 0)

    def angle_between_vectors(self, vector_a, vector_b):
        """Calculate the angle (in degrees) between two vectors."""
        cos_angle = self.dot_product(vector_a, vector_b) / (self.vector_magnitude(vector_a) * self.vector_magnitude(vector_b))
        return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

    def linear_interpolation(self, point_a, point_b, t):
        """Perform linear interpolation between two points."""
        return point_a + t * (point_b - point_a)

    def barycentric_coordinates(self, point, triangle_points):
        """Calculate barycentric coordinates of a point relative to a triangle."""
        a, b, c = triangle_points
        area_abc = self.calculate_area_of_triangle(a, b, c)
        area_abp = self.calculate_area_of_triangle(a, b, point)
        area_acp = self.calculate_area_of_triangle(a, c, point)
        area_bcp = self.calculate_area_of_triangle(b, c, point)
        return (area_abp / area_abc, area_acp / area_abc, area_bcp / area_abc)

    def transform_point(self, point, matrix):
        """Transform a point using a transformation matrix."""
        return np.dot(matrix, np.append(point, 1))[:2]

    def calculate_triangle_angles(self, point_a, point_b, point_c):
        """Calculate angles of a triangle formed by three points."""
        a = self.distance_between_points(point_b, point_c)
        b = self.distance_between_points(point_a, point_c)
        c = self.distance_between_points(point_a, point_b)
        angle_A = np.degrees(np.arccos((b**2 + c**2 - a**2) / (2 * b * c)))
        angle_B = np.degrees(np.arccos((a**2 + c**2 - b**2) / (2 * a * c)))
        angle_C = 180 - angle_A - angle_B
        return angle_A, angle_B, angle_C

    def calculate_vector_angle(self, vector_a, vector_b):
        """Calculate the angle between two vectors in degrees."""
        dot_product = np.dot(vector_a, vector_b)
        magnitudes = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        return np.degrees(np.arccos(dot_product / magnitudes))

    def calculate_diagonal_of_rectangle(self, width, height):
        """Calculate the diagonal length of a rectangle given its width and height."""
        return np.sqrt(width**2 + height**2)

    def centroid_of_polygon(self, polygon_points):
        """Calculate the centroid of a polygon given its vertices."""
        n = len(polygon_points)
        area = self.calculate_area_of_triangle(polygon_points[0], polygon_points[1], polygon_points[2])
        Cx = 0
        Cy = 0
        for i in range(n):
            x0 = polygon_points[i][0]
            y0 = polygon_points[i][1]
            x1 = polygon_points[(i + 1) % n][0]
            y1 = polygon_points[(i + 1) % n][1]
            factor = (x0 * y1 - x1 * y0)
            Cx += (x0 + x1) * factor
            Cy += (y0 + y1) * factor
        area *= 0.5
        Cx /= (6.0 * area)
        Cy /= (6.0 * area)
        return np.array([Cx, Cy])

    def is_point_on_line_segment(self, point, line_point_a, line_point_b):
        """Check if a point is on the line segment defined by two points."""
        return (min(line_point_a[0], line_point_b[0]) <= point[0] <= max(line_point_a[0], line_point_b[0]) and
                min(line_point_a[1], line_point_b[1]) <= point[1] <= max(line_point_a[1], line_point_b[1]) and
                np.isclose(self.calculate_area_of_triangle(line_point_a, line_point_b, point), 0))

    def calculate_reflection(self, point, line_point_a, line_point_b):
        """Calculate the reflection of a point across a line defined by two points."""
        projection = self.project_point_onto_line(point, line_point_a, line_point_b)
        return 2 * projection - point

    def transform_polygon(self, polygon_points, transformation_matrix):
        """Transform a polygon using a transformation matrix."""
        return [self.transform_point(point, transformation_matrix) for point in polygon_points]

    def calculate_angle_of_line(self, point_a, point_b):
        """Calculate the angle of the line connecting two points relative to the x-axis."""
        delta_y = point_b[1] - point_a[1]
        delta_x = point_b[0] - point_a[0]
        return np.degrees(np.arctan2(delta_y, delta_x))

    def calculate_euclidean_distance(self, point_a, point_b):
        """Calculate the Euclidean distance between two points."""
        return np.linalg.norm(point_a - point_b)

    def check_intersection(self, line1_start, line1_end, line2_start, line2_end):
        """Check if two line segments intersect."""
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        return (ccw(line1_start, line2_start, line2_end) != ccw(line1_end, line2_start, line2_end) and
                ccw(line1_start, line1_end, line2_start) != ccw(line1_start, line1_end, line2_end))

    def calculate_area_of_rectangle(self, width, height):
        """Calculate the area of a rectangle given its width and height."""
        return width * height

    def calculate_area_of_circle(self, radius):
        """Calculate the area of a circle given its radius."""
        return np.pi * radius**2

    def calculate_area_of_ellipse(self, a, b):
        """Calculate the area of an ellipse given its semi-major (a) and semi-minor (b) axes."""
        return np.pi * a * b

    def calculate_circumradius(self, point_a, point_b, point_c):
        """Calculate the circumradius of a triangle formed by three points."""
        a = self.distance_between_points(point_b, point_c)
        b = self.distance_between_points(point_a, point_c)
        c = self.distance_between_points(point_a, point_b)
        return (a * b * c) / (4 * self.calculate_area_of_triangle(point_a, point_b, point_c))

    def calculate_inradius(self, point_a, point_b, point_c):
        """Calculate the inradius of a triangle formed by three points."""
        area = self.calculate_area_of_triangle(point_a, point_b, point_c)
        s = (self.distance_between_points(point_a, point_b) + self.distance_between_points(point_b, point_c) + self.distance_between_points(point_c, point_a)) / 2
        return area / s

    def is_inside_polygon(self, point, polygon_points):
        """Check if a point is inside a polygon using the ray-casting algorithm."""
        n = len(polygon_points)
        inside = False
        p1x, p1y = polygon_points[0]
        for i in range(n + 1):
            p2x, p2y = polygon_points[i % n]
            if point[1] > min(p1y, p2y):
                if point[1] <= max(p1y, p2y):
                    if point[0] <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (point[1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or point[0] <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def calculate_median_of_polygon(self, polygon_points):
        """Calculate the median point of a polygon given its vertices."""
        n = len(polygon_points)
        x_coords = [point[0] for point in polygon_points]
        y_coords = [point[1] for point in polygon_points]
        return np.mean(x_coords), np.mean(y_coords)

    def calculate_area_of_regular_polygon(self, n_sides, side_length):
        """Calculate the area of a regular polygon given the number of sides and the length of each side."""
        return (n_sides * side_length**2) / (4 * np.tan(np.pi / n_sides))

    def calculate_distance_from_point_to_line(self, point, line_point_a, line_point_b):
        """Calculate the distance from a point to a line defined by two points."""
        line_vector = line_point_b - line_point_a
        point_vector = point - line_point_a
        line_length = self.vector_magnitude(line_vector)
        if line_length == 0:
            return self.distance_between_points(point, line_point_a)
        return np.abs(np.cross(line_vector, point_vector)) / line_length

    def calculate_slope_of_perpendicular(self, point_a, point_b):
        """Calculate the slope of the line perpendicular to the line defined by two points."""
        slope = self.calculate_slope(point_a, point_b)
        if slope == 0:
            return float('inf')  # Perpendicular to a horizontal line
        return -1 / slope

    def area_of_triangle_formed_by_points(self, point_a, point_b, point_c):
        """Calculate the area of a triangle given three points using the determinant method."""
        return 0.5 * abs(point_a[0] * (point_b[1] - point_c[1]) +
                          point_b[0] * (point_c[1] - point_a[1]) +
                          point_c[0] * (point_a[1] - point_b[1]))

    def is_point_in_circle(self, point, circle_center, radius):
        """Check if a point is inside a circle."""
        return self.distance_between_points(point, circle_center) <= radius

    def calculate_perimeter_of_polygon(self, polygon_points):
        """Calculate the perimeter of a polygon given its vertices."""
        perimeter = 0
        n = len(polygon_points)
        for i in range(n):
            perimeter += self.distance_between_points(polygon_points[i], polygon_points[(i + 1) % n])
        return perimeter

    def calculate_centroid_of_triangle(self, point_a, point_b, point_c):
        """Calculate the centroid of a triangle formed by three points."""
        return (point_a + point_b + point_c) / 3

    def calculate_normal_vector(self, point_a, point_b):
        """Calculate the normal vector to the line segment defined by two points."""
        return np.array([-(point_b[1] - point_a[1]), point_b[0] - point_a[0]])

    def calculate_angle_between_vectors(self, vector_a, vector_b):
        """Calculate the angle between two vectors in degrees."""
        cos_theta = np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
        return np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

    def project_point_onto_line(self, point, line_point_a, line_point_b):
        """Project a point onto a line defined by two points."""
        line_vector = line_point_b - line_point_a
        line_unit_vector = line_vector / np.linalg.norm(line_vector)
        return line_point_a + np.dot(point - line_point_a, line_unit_vector) * line_unit_vector

    def calculate_reflection_point(self, point, line_point_a, line_point_b):
        """Calculate the reflection point of a point over a line defined by two points."""
        projection = self.project_point_onto_line(point, line_point_a, line_point_b)
        return 2 * projection - point

    def calculate_area_of_trapezoid(self, base1, base2, height):
        """Calculate the area of a trapezoid given its two bases and height."""
        return 0.5 * (base1 + base2) * height

    def calculate_centroid_of_polygon(self, polygon_points):
        """Calculate the centroid of a polygon given its vertices."""
        n = len(polygon_points)
        Cx = 0
        Cy = 0
        signed_area = 0
        for i in range(n):
            x0, y0 = polygon_points[i]
            x1, y1 = polygon_points[(i + 1) % n]
            a = x0 * y1 - x1 * y0
            signed_area += a
            Cx += (x0 + x1) * a
            Cy += (y0 + y1) * a
        signed_area *= 0.5
        Cx /= (6.0 * signed_area)
        Cy /= (6.0 * signed_area)
        return np.array([Cx, Cy])

    def calculate_distance_between_lines(self, line1_point_a, line1_point_b, line2_point_a, line2_point_b):
        """Calculate the minimum distance between two lines defined by two points each."""
        def point_to_line_distance(point, line_point_a, line_point_b):
            line_vector = line_point_b - line_point_a
            point_vector = point - line_point_a
            line_length = np.linalg.norm(line_vector)
            if line_length == 0:
                return np.linalg.norm(point - line_point_a)
            return np.abs(np.cross(line_vector, point_vector)) / line_length

        distances = [
            point_to_line_distance(line1_point_a, line2_point_a, line2_point_b),
            point_to_line_distance(line1_point_b, line2_point_a, line2_point_b),
            point_to_line_distance(line2_point_a, line1_point_a, line1_point_b),
            point_to_line_distance(line2_point_b, line1_point_a, line1_point_b)
        ]
        return min(distances)

    def area_of_parallelogram(self, base, height):
        """Calculate the area of a parallelogram given its base and height."""
        return base * height

    def rotate_polygon(self, polygon_points, angle):
        """Rotate a polygon by a given angle around the origin."""
        return [self.rotate_point(point, angle) for point in polygon_points]

    def mean_of_data_points(self):
        """Calculate the mean of the data points."""
        return np.mean(self.data_points)

    def calculate_skewness(self):
        """Calculate the skewness of the data points."""
        if len(self.data_points) < 3:
            raise ValueError("At least three data points are required to calculate skewness.")
        
        mean = self.mean_of_data_points()
        deviations = np.array(self.data_points) - mean
        skewness = (
            len(self.data_points) / ((len(self.data_points) - 1) * (len(self.data_points) - 2))
        ) * np.sum((deviations ** 3) / (np.std(self.data_points, ddof=1) ** 3))
        
        return skewness

    def calculate_area_of_trapezoid(self, base1, base2, height):
        """Calculate the area of a trapezoid given its bases and height."""
        return 0.5 * (base1 + base2) * height

    def calculate_volume_of_cylinder(self, radius, height):
        """Calculate the volume of a cylinder given its radius and height."""
        return np.pi * radius**2 * height

    def calculate_volume_of_cone(self, radius, height):
        """Calculate the volume of a cone given its radius and height."""
        return (1/3) * np.pi * radius**2 * height

    def calculate_volume_of_sphere(self, radius):
        """Calculate the volume of a sphere given its radius."""
        return (4/3) * np.pi * radius**3

    def calculate_distance_between_lines(self, line1_point_a, line1_point_b, line2_point_a, line2_point_b):
        """Calculate the distance between two lines defined by two points each."""
        # Use the formula to find the distance between two lines
        def line_vector(line_point_a, line_point_b):
            return line_point_b - line_point_a

        line1_vec = line_vector(line1_point_a, line1_point_b)
        line2_vec = line_vector(line2_point_a, line2_point_b)

        if np.isclose(np.cross(line1_vec, line2_vec), 0):
            # Lines are parallel
            return self.calculate_distance_from_point_to_line(line1_point_a, line2_point_a, line2_point_b)
        
        # Calculate the intersection point
        direction = np.cross(line1_vec, line2_vec)
        intersection = line1_point_a + (np.dot(line2_point_a - line1_point_a, line2_vec) / np.dot(line1_vec, line2_vec)) * line1_vec
        
        # Return the distance from the intersection to one of the lines
        return self.distance_between_points(intersection, line1_point_a)


