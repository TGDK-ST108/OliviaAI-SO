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