import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.path import Path

class Mahadevi:
    def __init__(self):
        self.vector_field = []

    def set_vector_field(self, vectors):
        """Set the vector field with a list of vectors."""
        self.vector_field = vectors

    def clear_vector_field(self):
        """Clear the vector field."""
        self.vector_field = []

    def list_vector_field(self):
        """List all vectors in the vector field."""
        print("Current Vector Field:")
        for i, vector in enumerate(self.vector_field):
            print(f"Vector {i}: {vector}")

    def print_vector_field_info(self):
        """Print details of vectors in the field."""
        print(f"Total vectors in the field: {len(self.vector_field)}")
        for i, vector in enumerate(self.vector_field):
            print(f"Vector {i}: {vector}, Magnitude: {self.compute_vector_magnitude(vector)}")

    def save_vector_field(self, filename):
        """Save the vector field to a file."""
        np.savetxt(filename, self.vector_field)
        print(f"Vector field saved to '{filename}'.")

    def load_vector_field(self, filename):
        """Load the vector field from a file."""
        self.vector_field = np.loadtxt(filename).tolist()
        print(f"Vector field loaded from '{filename}'.")

# Vector Operations
    def add_vectors(self, vector_a, vector_b):
        """Add two vectors."""
        return np.add(vector_a, vector_b)

    def subtract_vectors(self, vector_a, vector_b):
        """Subtract vector b from vector a."""
        return np.subtract(vector_a, vector_b)

    def scalar_multiply(self, vector, scalar):
        """Multiply a vector by a scalar."""
        return np.multiply(vector, scalar)

    def dot_product(self, vector_a, vector_b):
        """Calculate the dot product of two vectors."""
        return np.dot(vector_a, vector_b)

    def cross_product(self, vector_a, vector_b):
        """Calculate the cross product of two 3D vectors."""
        return np.cross(vector_a, vector_b)

    def compute_vector_magnitude(self, vector):
        """Compute the magnitude (length) of a vector."""
        return np.linalg.norm(vector)

    def normalize_vector(self, vector):
        """Normalize a vector to unit length."""
        magnitude = self.compute_vector_magnitude(vector)
        if magnitude == 0:
            raise ValueError("Cannot normalize the zero vector.")
        return vector / magnitude

    def angle_between_vectors(self, vector_a, vector_b):
        """Calculate the angle between two vectors in degrees."""
        dot_product = self.dot_product(vector_a, vector_b)
        magnitudes = self.compute_vector_magnitude(vector_a) * self.compute_vector_magnitude(vector_b)
        return np.degrees(np.arccos(dot_product / magnitudes))

    def compute_angle_between_vectors(self, vector_a, vector_b):
        """Calculate the angle between two vectors in radians."""
        dot_product = self.dot_product(vector_a, vector_b)
        magnitudes = self.compute_vector_magnitude(vector_a) * self.compute_vector_magnitude(vector_b)
        return np.arccos(dot_product / magnitudes)

    def is_orthogonal(self, vector_a, vector_b):
        """Check if two vectors are orthogonal (dot product = 0)."""
        return np.isclose(self.dot_product(vector_a, vector_b), 0)

    def is_parallel(self, vector_a, vector_b):
        """Check if two vectors are parallel."""
        return np.allclose(self.cross_product(vector_a, vector_b), 0)

    def project_vector_onto_vector(self, vector_a, vector_b):
        """Project vector_a onto vector_b."""
        unit_b = self.normalize_vector(vector_b)
        return self.dot_product(vector_a, unit_b) * unit_b

    def project_vector_onto_plane(self, vector, normal):
        """Project a vector onto a plane defined by a normal vector."""
        return vector - self.project_vector_onto_vector(vector, normal)

    def reflect_vector(self, vector, normal):
        """Reflect a vector across a given normal vector."""
        return vector - 2 * self.dot_product(vector, normal) * normal

    def generate_random_vector(self, size):
        """Generate a random vector of specified size."""
        return np.random.rand(size)

    def generate_unit_vector(self, size):
        """Generate a random unit vector of specified size."""
        return self.normalize_vector(self.generate_random_vector(size))

    def rotate_vector(self, vector, angle):
        """Rotate a 2D vector by a specified angle in degrees."""
        theta = np.radians(angle)
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta),  np.cos(theta)]])
        return np.dot(rotation_matrix, vector)

# Matrix Operations
    def transpose_matrix(self, matrix):
        """Transpose a given matrix."""
        return np.transpose(matrix)

    def matrix_multiplication(self, matrix_a, matrix_b):
        """Multiply two matrices."""
        return np.matmul(matrix_a, matrix_b)

    def inverse_matrix(self, matrix):
        """Calculate the inverse of a matrix."""
        return np.linalg.inv(matrix)

    def determinant_matrix(self, matrix):
        """Calculate the determinant of a matrix."""
        return np.linalg.det(matrix)

    def eigenvalues_and_vectors(self, matrix):
        """Calculate eigenvalues and eigenvectors of a matrix."""
        return np.linalg.eig(matrix)

    def matrix_rank(self, matrix):
        """Calculate the rank of a matrix."""
        return np.linalg.matrix_rank(matrix)

    def create_identity_matrix(self, size):
        """Create an identity matrix of a given size."""
        return np.eye(size)

    def check_matrix_square(self, matrix):
        """Check if a matrix is square."""
        return matrix.shape[0] == matrix.shape[1]

    def flatten_matrix(self, matrix):
        """Flatten a 2D matrix into a 1D array."""
        return matrix.flatten()

    def generate_diagonal_matrix(self, diagonal_elements):
        """Generate a diagonal matrix from a list of diagonal elements."""
        return np.diag(diagonal_elements)

    def check_matrix_symmetry(self, matrix):
        """Check if a matrix is symmetric."""
        return np.allclose(matrix, matrix.T)

    def is_invertible(self, matrix):
        """Check if a matrix is invertible."""
        return np.linalg.cond(matrix) < 1 / np.finfo(matrix.dtype).eps

    def calculate_trace_of_matrix(self, matrix):
        """Calculate the trace of a matrix."""
        return np.trace(matrix)

    def calculate_covariance_matrix(self, vectors):
        """Calculate the covariance matrix from a list of vectors."""
        return np.cov(np.array(vectors).T)

    def calculate_correlation_matrix(self, vectors):
        """Calculate the correlation matrix from a list of vectors."""
        return np.corrcoef(np.array(vectors).T)

    def calculate_adjoint_matrix(self, matrix):
        """Calculate the adjoint of a matrix."""
        return np.linalg.inv(matrix).T * np.linalg.det(matrix)

    def calculate_symmetric_part(self, matrix):
        """Calculate the symmetric part of a matrix."""
        return 0.5 * (matrix + matrix.T)

    def calculate_skew_symmetric_part(self, matrix):
        """Calculate the skew-symmetric part of a matrix."""
        return 0.5 * (matrix - matrix.T)

    def compute_kronecker_product(self, matrix_a, matrix_b):
        """Compute the Kronecker product of two matrices."""
        return np.kron(matrix_a, matrix_b)

    def compute_hadamard_product(self, matrix_a, matrix_b):
        """Compute the Hadamard product of two matrices."""
        return np.multiply(matrix_a, matrix_b)

    def calculate_cholesky_decomposition(self, matrix):
        """Calculate the Cholesky decomposition of a positive definite matrix."""
        return np.linalg.cholesky(matrix)

    def compute_pseudo_inverse(self, matrix):
        """Compute the pseudo-inverse of a matrix."""
        return np.linalg.pinv(matrix)

    def calculate_matrix_product(self, matrix_a, matrix_b):
        """Calculate the product of two matrices."""
        return self.matrix_multiplication(matrix_a, matrix_b)

    def calculate_matrix_square(self, matrix):
        """Calculate the square of a matrix."""
        return self.matrix_multiplication(matrix, matrix)

    def generate_permutation_matrix(self, n):
        """Generate a random permutation matrix of size n."""
        return np.eye(n)[np.random.permutation(n)]

    def rotate_matrix(self, matrix, angle):
        """Rotate a 2D matrix by a given angle in degrees."""
        theta = np.radians(angle)
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta),  np.cos(theta)]])
        return self.matrix_multiplication(rotation_matrix, matrix)

    def check_if_matrix_is_stochastic(self, matrix):
        """Check if a matrix is stochastic (rows sum to 1)."""
        return np.allclose(np.sum(matrix, axis=1), 1)

    def check_if_matrix_is_positive_definite(self, matrix):
        """Check if a matrix is positive definite."""
        return np.all(np.linalg.eigvals(matrix) > 0)

    def calculate_condition_number(self, matrix):
        """Calculate the condition number of a matrix."""
        return np.linalg.cond(matrix)

    def calculate_frobenius_norm(self, matrix):
        """Calculate the Frobenius norm of a matrix."""
        return np.linalg.norm(matrix, 'fro')

    def calculate_distance_between_matrices(self, matrix_a, matrix_b):
        """Compute the Frobenius distance between two matrices."""
        return np.linalg.norm(matrix_a - matrix_b, 'fro')

# Statistical Operations
    def mean_vector(self, vector):
        """Calculate the mean of a vector."""
        return np.mean(vector)

    def median_vector(self, vector):
        """Calculate the median of a vector."""
        return np.median(vector)

    def variance_vector(self, vector):
        """Calculate the variance of a vector."""
        return np.var(vector)

    def standard_deviation_vector(self, vector):
        """Calculate the standard deviation of a vector."""
        return np.std(vector)

    def correlation_coefficient(self, vector_a, vector_b):
        """Calculate the correlation coefficient between two vectors."""
        return np.corrcoef(vector_a, vector_b)[0, 1]

    def compute_geometric_mean(self, vector):
        """Calculate the geometric mean of a vector."""
        return np.prod(vector) ** (1 / len(vector))

    def compute_harmonic_mean(self, vector):
        """Calculate the harmonic mean of a vector."""
        return len(vector) / np.sum(1.0 / np.array(vector))

    # Projection Operations
    def project_vector_onto_vector(self, vector_a, vector_b):
        """Project vector a onto vector b."""
        unit_b = self.normalize_vector(vector_b)
        return self.dot_product(vector_a, unit_b) * unit_b

    def project_vector_onto_plane(self, vector, normal):
        """Project a vector onto a plane defined by a normal vector."""
        return vector - self.project_vector_onto_vector(vector, normal)

    def distance_from_point_to_line(self, point, line_point1, line_point2):
        """Calculate the distance from a point to a line segment."""
        line_vec = self.subtract_vectors(line_point2, line_point1)
        point_vec = self.subtract_vectors(point, line_point1)
        line_len = self.compute_vector_magnitude(line_vec)
        line_unit_vec = self.normalize_vector(line_vec)
        projection = self.dot_product(point_vec, line_unit_vec)
        return self.compute_vector_magnitude(self.subtract_vectors(point_vec, line_unit_vec * projection))

    def calculate_inner_product(self, vector_a, vector_b):
        """Calculate the inner product of two vectors."""
        return np.inner(vector_a, vector_b)

    def calculate_outer_product(self, vector_a, vector_b):
        """Calculate the outer product of two vectors."""
        return np.outer(vector_a, vector_b)

    def calculate_distance_from_point_to_subspace(self, point, subspace_basis):
        """Calculate the distance from a point to a subspace defined by a basis."""
        projection = np.sum([self.project_vector_onto_vector(point, basis) for basis in subspace_basis], axis=0)
        return self.compute_vector_magnitude(self.subtract_vectors(point, projection))

    def calculate_vector_projection(self, vector_a, vector_b):
        """Compute the vector projection of vector_a onto vector_b."""
        return self.project_vector_onto_vector(vector_a, vector_b)

    def check_if_vectors_are_coplanar(self, vector_a, vector_b, vector_c):
        """Check if three vectors are coplanar."""
        return np.isclose(self.dot_product(self.cross_product(vector_a, vector_b), vector_c), 0)

# Geometric and Spatial Operations
    def distance_between_points(self, point_a, point_b):
        """Calculate the Euclidean distance between two points."""
        return np.linalg.norm(np.subtract(point_a, point_b))

    def area_of_triangle(self, vertex_a, vertex_b, vertex_c):
        """Calculate the area of a triangle using its vertices."""
        ab = self.subtract_vectors(vertex_b, vertex_a)
        ac = self.subtract_vectors(vertex_c, vertex_a)
        return 0.5 * self.compute_vector_magnitude(self.cross_product(ab, ac))

    def compute_area_of_polygon(self, vertices):
        """Calculate the area of a polygon using the Shoelace formula."""
        vertices = np.array(vertices)
        return 0.5 * np.abs(np.dot(vertices[:, 0], np.roll(vertices[:, 1], 1)) -
                            np.dot(vertices[:, 1], np.roll(vertices[:, 0], 1)))

    def calculate_signed_area_of_polygon(self, vertices):
        """Calculate the signed area of a polygon defined by its vertices."""
        vertices = np.array(vertices)
        n = len(vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
        return 0.5 * area

    def calculate_area_of_triangle_from_coordinates(self, vertex_a, vertex_b, vertex_c):
        """Calculate the area of a triangle given its vertices."""
        return 0.5 * np.abs((vertex_a[0] * (vertex_b[1] - vertex_c[1]) +
                             vertex_b[0] * (vertex_c[1] - vertex_a[1]) +
                             vertex_c[0] * (vertex_a[1] - vertex_b[1])))

    def area_of_parallelogram(self, vertex_a, vertex_b, vertex_c):
        """Calculate the area of a parallelogram given its vertices."""
        ab = self.subtract_vectors(vertex_b, vertex_a)
        ac = self.subtract_vectors(vertex_c, vertex_a)
        return self.compute_vector_magnitude(self.cross_product(ab, ac))

    def point_in_polygon(self, point, polygon):
        """Check if a point is inside a given polygon."""
        path = Path(polygon)
        return path.contains_point(point)

    def calculate_centroid_of_polygon(self, vertices):
        """Calculate the centroid of a polygon defined by its vertices."""
        vertices = np.array(vertices)
        x = vertices[:, 0]
        y = vertices[:, 1]
        A = 0.5 * (np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        C_x = (1 / (6 * A)) * np.dot(x + np.roll(x, 1), np.roll(y, 1) - y)
        C_y = (1 / (6 * A)) * np.dot(y + np.roll(y, 1), x - np.roll(x, 1))
        return np.array([C_x, C_y])

    def calculate_center_of_mass_of_polygon(self, vertices):
        """Calculate the center of mass of a polygon defined by its vertices."""
        area = self.compute_area_of_polygon(vertices)
        cx = 0
        cy = 0
        for i in range(len(vertices)):
            x_i, y_i = vertices[i]
            x_next, y_next = vertices[(i + 1) % len(vertices)]
            common = x_i * y_next - x_next * y_i
            cx += (x_i + x_next) * common
            cy += (y_i + y_next) * common
        cx /= (6 * area)
        cy /= (6 * area)
        return np.array([cx, cy])

    def calculate_barycentric_coordinates(self, point, vertices):
        """Calculate the barycentric coordinates of a point w.r.t. triangle vertices."""
        a, b, c = vertices
        v0 = b - a
        v1 = c - a
        v2 = point - a
        d00 = np.dot(v0, v0)
        d01 = np.dot(v0, v1)
        d11 = np.dot(v1, v1)
        d20 = np.dot(v2, v0)
        d21 = np.dot(v2, v1)
        denom = d00 * d11 - d01 * d01
        v = (d11 * d20 - d01 * d21) / denom
        w = (d00 * d21 - d01 * d20) / denom
        return np.array([1 - v - w, v, w])

    def calculate_closest_point_on_line_segment(self, point, line_point1, line_point2):
        """Calculate the closest point on a line segment to a given point."""
        line_vec = self.subtract_vectors(line_point2, line_point1)
        t = self.dot_product(self.subtract_vectors(point, line_point1), line_vec) / self.dot_product(line_vec, line_vec)
        if t < 0:
            return line_point1
        elif t > 1:
            return line_point2
        else:
            return line_point1 + t * line_vec

    def calculate_dihedral_angle(self, normal_a, normal_b):
        """Calculate the dihedral angle between two planes defined by their normals."""
        cosine_angle = self.dot_product(normal_a, normal_b) / (self.compute_vector_magnitude(normal_a) * self.compute_vector_magnitude(normal_b))
        return np.arccos(cosine_angle)

    def compute_normal_vector_to_plane(self, point1, point2, point3):
        """Compute the normal vector to a plane defined by three points."""
        vector_a = self.subtract_vectors(point2, point1)
        vector_b = self.subtract_vectors(point3, point1)
        return self.cross_product(vector_a, vector_b)

def calculate_volume_of_prism(self, base_area, height):
        """Calculate the volume of a prism given its base area and height."""
        return base_area * height

    def calculate_surface_area_of_prism(self, base_area, perimeter, height):
        """Calculate the surface area of a prism."""
        return 2 * base_area + perimeter * height

    def calculate_volume_of_pyramid(self, base_area, height):
        """Calculate the volume of a pyramid."""
        return (1 / 3) * base_area * height

    def calculate_surface_area_of_pyramid(self, base_area, slant_height, base_perimeter):
        """Calculate the surface area of a pyramid."""
        return base_area + (base_perimeter * slant_height) / 2

    def calculate_volume_of_cone(self, radius, height):
        """Calculate the volume of a cone."""
        return (1 / 3) * np.pi * radius**2 * height

    def calculate_surface_area_of_cone(self, radius, slant_height):
        """Calculate the surface area of a cone."""
        return np.pi * radius * (radius + slant_height)

    def calculate_volume_of_cylinder(self, radius, height):
        """Calculate the volume of a cylinder."""
        return np.pi * radius**2 * height

    def calculate_surface_area_of_cylinder(self, radius, height):
        """Calculate the surface area of a cylinder."""
        return 2 * np.pi * radius * (radius + height)

    def calculate_volume_of_sphere(self, radius):
        """Calculate the volume of a sphere."""
        return (4 / 3) * np.pi * radius**3

    def calculate_surface_area_of_sphere(self, radius):
        """Calculate the surface area of a sphere."""
        return 4 * np.pi * radius**2

    def calculate_volume_of_torus(self, major_radius, minor_radius):
        """Calculate the volume of a torus."""
        return (2 * np.pi * minor_radius) * (np.pi * major_radius**2)

    def calculate_surface_area_of_torus(self, major_radius, minor_radius):
        """Calculate the surface area of a torus."""
        return (2 * np.pi * minor_radius) * (2 * np.pi * major_radius)

    def calculate_volume_of_ellipsoid(self, semi_major_axis, semi_minor_axis):
        """Calculate the volume of an ellipsoid."""
        return (4 / 3) * np.pi * semi_major_axis * semi_minor_axis**2

    def calculate_surface_area_of_ellipsoid(self, semi_major_axis, semi_minor_axis):
        """Approximate surface area of ellipsoid using Knud Thomsen's formula."""
        p = 1.6075
        a = semi_major_axis
        b = semi_minor_axis
        return 4 * np.pi * ((a**p * b**p)**(1/p))

    def calculate_volume_of_tetrahedron(self, vertices):
        """Calculate the volume of a tetrahedron defined by four vertices."""
        return abs(np.linalg.det(np.hstack((vertices, np.ones((4, 1))))) / 6)

    def calculate_volume_of_frustum(self, base_area1, base_area2, height):
        """Volume of frustum (trapezoidal prism shape)."""
        return (1 / 3) * height * (base_area1 + base_area2 + np.sqrt(base_area1 * base_area2))

    def calculate_surface_area_of_frustum(self, base_area1, base_area2, slant_height):
        """Surface area of frustum using base areas and slant height."""
        return base_area1 + base_area2 + (base_area1 + base_area2) * slant_height

    def calculate_volume_of_spherical_cap(self, radius, height):
        """Calculate the volume of a spherical cap."""
        return (1 / 3) * np.pi * height**2 * (3 * radius - height)

    def calculate_surface_area_of_spherical_cap(self, radius, height):
        """Surface area of a spherical cap."""
        return 2 * np.pi * radius * height

    def calculate_volume_of_polygonal_prism(self, vertices, height):
        """Volume of prism with polygonal base."""
        base_area = self.compute_area_of_polygon(vertices)
        return base_area * height

    def calculate_surface_area_of_polygonal_prism(self, vertices, height):
        """Surface area of prism with polygonal base."""
        base_area = self.compute_area_of_polygon(vertices)
        perimeter = np.sum([
            self.distance_between_points(vertices[i], vertices[(i + 1) % len(vertices)])
            for i in range(len(vertices))
        ])
        return 2 * base_area + perimeter * height

    def calculate_volume_of_polygonal_frustum(self, base_area1, base_area2, height):
        """Volume of polygonal frustum."""
        return (1 / 3) * height * (base_area1 + base_area2 + np.sqrt(base_area1 * base_area2))

    def calculate_surface_area_of_polygonal_frustum(self, base_area1, base_area2, slant_height):
        """Surface area of polygonal frustum."""
        return base_area1 + base_area2 + (base_area1 + base_area2) * slant_height

# Moment of Inertia Calculations
    def calculate_moment_of_inertia_of_circle(self, radius):
        """Moment of inertia of a circle about its center."""
        return 0.5 * np.pi * radius**4

    def calculate_moment_of_inertia_of_rectangle(self, width, height):
        """Moment of inertia of a rectangle about its base."""
        return (1 / 12) * width * height**3

    def calculate_moment_of_inertia_of_triangle(self, base, height):
        """Moment of inertia of a triangle about its base."""
        return (1 / 36) * base * height**3

    def calculate_moment_of_inertia_of_solid_sphere(self, radius):
        """Moment of inertia of a solid sphere."""
        return (2 / 5) * ((4 / 3) * np.pi * radius**3) * radius**2

    def calculate_moment_of_inertia_of_cylinder(self, radius, height):
        """Moment of inertia of a solid cylinder."""
        return (1 / 12) * np.pi * radius**2 * height * (3 * radius**2 + height**2)

    def calculate_moment_of_inertia_of_pyramid(self, base_area, height):
        """Approximate moment of inertia of a pyramid."""
        return (1 / 10) * base_area * height**2

    def calculate_moments_of_inertia_of_polygonal_shape(self, vertices):
        """Approximate moments of inertia for a polygonal 2D shape."""
        I_x = 0
        I_y = 0
        A = self.compute_area_of_polygon(vertices)
        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            I_x += (vertices[i][1]**2 + vertices[j][1]**2) * (vertices[j][0] - vertices[i][0])
            I_y += (vertices[i][0]**2 + vertices[j][0]**2) * (vertices[j][1] - vertices[i][1])
        return (1 / 12) * A, (1 / 12) * A

    def calculate_inertia_tensor(self, vertices):
        """Calculate the inertia tensor of a polygon."""
        inertia_tensor = np.zeros((2, 2))
        vertices = np.array(vertices)
        for i in range(len(vertices)):
            v = vertices[i]
            next_v = vertices[(i + 1) % len(vertices)]
            cross = np.cross(v, next_v)
            inertia_tensor += (cross / 2) * (np.outer(v, v) + np.outer(v, next_v) + np.outer(next_v, next_v))
        return inertia_tensor

    # Coordinate Conversions
    def calculate_polar_coordinates(self, point):
        """Convert Cartesian to polar coordinates."""
        r = np.sqrt(point[0]**2 + point[1]**2)
        theta = np.arctan2(point[1], point[0])
        return np.array([r, theta])

    def calculate_cartesian_coordinates_from_polar(self, polar_coordinates):
        """Convert polar to Cartesian coordinates."""
        r, theta = polar_coordinates
        return np.array([r * np.cos(theta), r * np.sin(theta)])

    def compute_spherical_coordinates(self, point):
        """Convert Cartesian to spherical coordinates."""
        r = self.compute_vector_magnitude(point)
        theta = np.arccos(point[2] / r)
        phi = np.arctan2(point[1], point[0])
        return np.array([r, theta, phi])

    def compute_cartesian_coordinates(self, spherical_coordinates):
        """Convert spherical to Cartesian coordinates."""
        r, theta, phi = spherical_coordinates
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return np.array([x, y, z])

    def calculate_spherical_coordinates_of_polygon(self, vertices):
        """Convert polygon vertices to spherical coordinates."""
        return np.array([self.compute_spherical_coordinates(vertex) for vertex in vertices])

    def calculate_cartesian_coordinates_of_polygon(self, spherical_coordinates):
        """Convert spherical coordinates of polygon to Cartesian."""
        return np.array([self.compute_cartesian_coordinates(coord) for coord in spherical_coordinates])

    def check_if_point_is_in_polyhedron(self, point, vertices):
        """Check if a point is inside a polyhedron defined by vertices."""
        hull = ConvexHull(vertices)
        new_points = np.vstack([vertices, point])
        new_hull = ConvexHull(new_points)
        return np.array_equal(hull.vertices, new_hull.vertices)

    def calculate_volume_of_polyhedron(self, vertices):
        """Calculate the volume of a convex polyhedron using ConvexHull."""
        hull = ConvexHull(vertices)
        return hull.volume

    def calculate_signed_volume_of_polyhedron(self, vertices):
        """Compute the signed volume of a polyhedron using tetrahedral decomposition."""
        volume = 0
        for i in range(len(vertices) - 2):
            volume += np.dot(vertices[i], self.cross_product(vertices[i + 1], vertices[i + 2])) / 6
        return volume

    def calculate_distance_between_points_and_polyhedron(self, points, vertices):
        """Compute distance from each point to the polyhedron (returns 0 if inside)."""
        distances = []
        for point in points:
            if self.check_if_point_is_in_polyhedron(point, vertices):
                distances.append(0)
            else:
                normal = self.compute_normal_vector_to_plane(vertices[0], vertices[1], vertices[2])
                distances.append(self.distance_from_point_to_plane(point, vertices[0], normal))
        return distances

    def calculate_distance_between_tetrahedron_and_point(self, vertices, point):
        """Calculate the shortest distance from a point to a tetrahedron."""
        if self.check_if_point_is_in_polyhedron(point, vertices):
            return 0
        else:
            return min(
                self.distance_from_point_to_plane(point, vertices[i],
                    self.compute_normal_vector_to_plane(vertices[i], vertices[j], vertices[k]))
                for i in range(4) for j in range(i+1, 4) for k in range(j+1, 4)
            )

    def calculate_area_of_tetrahedron(self, vertices):
        """Calculate total surface area of tetrahedron (sum of all triangle faces)."""
        return sum(
            self.area_of_triangle(vertices[i], vertices[j], vertices[k])
            for i in range(4) for j in range(i+1, 4) for k in range(j+1, 4)
        )

    def calculate_intersection_of_lines(self, line1_point1, line1_point2, line2_point1, line2_point2):
        """Calculate the intersection point of two lines in space if they intersect."""
        A = np.array([line1_point2 - line1_point1, line2_point1 - line2_point2]).T
        b = line2_point1 - line1_point1
        if np.linalg.matrix_rank(A) < 2:
            return None  # Lines are parallel or coincident
        t = np.linalg.lstsq(A, b, rcond=None)[0]
        return line1_point1 + t[0] * (line1_point2 - line1_point1)

    def compute_intersection_of_two_planes(self, normal_a, d_a, normal_b, d_b):
        """Compute line of intersection of two planes."""
        direction = self.cross_product(normal_a, normal_b)
        if np.allclose(direction, 0):
            return None  # Planes are parallel
        A = np.array([normal_a, normal_b])
        b = np.array([d_a, d_b])
        point_on_line = np.linalg.lstsq(A, b, rcond=None)[0]
        return point_on_line, direction

    def compute_distance_between_point_and_plane(self, point, plane_normal, plane_d):
        """Distance from point to plane defined by normal and offset (Ax + By + Cz + D = 0)."""
        return abs(self.dot_product(point, plane_normal) + plane_d) / self.compute_vector_magnitude(plane_normal)

    def calculate_determinant_of_submatrix(self, matrix, rows, cols):
        """Compute determinant of a submatrix defined by row and column indices."""
        submatrix = matrix[np.ix_(rows, cols)]
        return np.linalg.det(submatrix)

    def compute_bilinear_form(self, matrix, vector_a, vector_b):
        """Compute bilinear form aᵀMb."""
        return self.dot_product(vector_a, self.matrix_multiplication(matrix, vector_b))

# OliviaAI / TGDK Hook Integrations
    def apply_olivia_symbolic_transform(self, vector, symbol_matrix):
        """Apply symbolic transformation using OliviaAI-style symbolic routing matrix."""
        return self.matrix_multiplication(symbol_matrix, vector)

    def olivia_vector_logic_gate(self, vector_a, vector_b, gate_type="XOR"):
        """Apply logical gate between two vectors (symbolic boolean logic)."""
        a = np.array(vector_a).astype(bool)
        b = np.array(vector_b).astype(bool)
        if gate_type == "XOR":
            return np.logical_xor(a, b).astype(int)
        elif gate_type == "AND":
            return np.logical_and(a, b).astype(int)
        elif gate_type == "OR":
            return np.logical_or(a, b).astype(int)
        elif gate_type == "NAND":
            return np.logical_not(np.logical_and(a, b)).astype(int)
        else:
            raise ValueError("Unsupported gate type.")

    def route_quantum_vector(self, vector, entropy_map):
        """Simulate quantum-routing behavior by probabilistically distorting a vector field."""
        noise = np.random.normal(loc=0.0, scale=entropy_map, size=len(vector))
        return np.add(vector, noise)

    def compute_quantum_entropy_signature(self, matrix):
        """Return the entropy signature (Shannon entropy-like) of a normalized matrix."""
        m = np.abs(matrix / np.sum(np.abs(matrix)))
        return -np.sum(m * np.log2(m + 1e-10))

    def symbolic_reduction(self, vector_field, symbol="⊗"):
        """Apply a symbolic folding operation over the vector field using a symbolic operator."""
        reduced = np.sum(vector_field, axis=0)
        print(f"Symbolic reduction [{symbol}] result: {reduced}")
        return reduced

    def quantize_vector_field(self, num_levels):
        """Quantize all vectors in the field to discrete symbolic levels."""
        quantized_field = []
        for vector in self.vector_field:
            q_vector = np.round(np.interp(vector, [min(vector), max(vector)], [0, num_levels - 1]))
            quantized_field.append(q_vector)
        return quantized_field

    def apply_custom_operation(self, func, *args, **kwargs):
        """General interface for injecting custom logic into Mahadevi class."""
        return func(*args, **kwargs)

    def export_vector_field_as_tensor(self):
        """Export the vector field as a multi-dimensional tensor (for ML/AI hooks)."""
        return np.stack(self.vector_field)

    def symbolic_tensor_product(self, matrix_a, matrix_b):
        """Compute a symbolic tensor product for pattern expansion."""
        return np.tensordot(matrix_a, matrix_b, axes=0)

    def set_vector_field_from_symbolic_pattern(self, pattern):
        """Set the vector field based on a predefined symbolic pattern (e.g., grid, wave, lattice)."""
        if pattern == "lattice3x3":
            self.vector_field = [[i, j, i*j] for i in range(3) for j in range(3)]
        elif pattern == "sinwave":
            self.vector_field = [[x, np.sin(x)] for x in np.linspace(0, 2*np.pi, 10)]
        else:
            raise ValueError("Pattern not recognized.")

    def generate_olivia_signature_token(self, seed_vector):
        """Generate an OliviaAI signature token from a vector input."""
        norm = self.normalize_vector(seed_vector)
        token = "-".join([f"{x:.3f}" for x in norm])
        return f"OLIVIA::SIG::{token}"

    def initialize_quantum_field_matrix(self, shape=(3, 3), seed=0.005):
        """Create a randomized quantum field matrix with minimal deterministic seed."""
        np.random.seed(int(seed * 1e6))
        return np.random.rand(*shape)

    def interpret_symbolic_interaction(self, vector_a, vector_b, symbol="†"):
        """Interpret a symbolic interaction between vectors with overlay marker."""
        merged = self.add_vectors(vector_a, vector_b)
        print(f"Symbol [{symbol}] interaction yields: {merged}")
        return merged