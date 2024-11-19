import numpy as np
from scipy.spatial import ConvexHull

class Mahadevi:
    def __init__(self):
        """Initialize the Mahadevi module with a vector field and essential matrix/vector operations."""
        self.vector_field = []

    def set_vector_field(self, vectors):
        """Set the vector field with a list of vectors."""
        self.vector_field = vectors
        print("Vector field set successfully.")

    # Data unfolding and transformation
    def unfold_data_with_matrix(self, data_matrix):
        """Unfold the data using a transformation matrix on the vector field."""
        if not self.vector_field:
            raise ValueError("Vector field is not set.")
        transformed_data = []
        for row in data_matrix:
            transformed_row = [
                sum(row[i] * self.vector_field[i][j] for i in range(len(row)))
                for j in range(len(self.vector_field[0]))
            ]
            transformed_data.append(transformed_row)
        print("Data unfolded successfully.")
        return transformed_data

    # Vector Operations
    def compute_vector_magnitude(self, vector):
        """Compute the magnitude of a vector."""
        return np.linalg.norm(vector)

    def normalize_vector(self, vector):
        """Normalize a vector to unit length."""
        magnitude = self.compute_vector_magnitude(vector)
        if magnitude == 0:
            raise ValueError("Cannot normalize the zero vector.")
        return vector / magnitude

    def add_vectors(self, vector_a, vector_b):
        """Add two vectors element-wise."""
        return np.add(vector_a, vector_b)

    def subtract_vectors(self, vector_a, vector_b):
        """Subtract vector b from vector a."""
        return np.subtract(vector_a, vector_b)

    def dot_product(self, vector_a, vector_b):
        """Compute the dot product of two vectors."""
        return np.dot(vector_a, vector_b)

    def cross_product(self, vector_a, vector_b):
        """Compute the cross product of two 3D vectors."""
        return np.cross(vector_a, vector_b)

    def angle_between_vectors(self, vector_a, vector_b):
        """Calculate the angle between two vectors in degrees."""
        dot_product = self.dot_product(vector_a, vector_b)
        magnitudes = self.compute_vector_magnitude(vector_a) * self.compute_vector_magnitude(vector_b)
        return np.degrees(np.arccos(dot_product / magnitudes))

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

    # Statistical Operations
    def mean_vector(self, vector):
        """Calculate the mean of elements in a vector."""
        return np.mean(vector)

    def variance_vector(self, vector):
        """Calculate the variance of elements in a vector."""
        return np.var(vector)

    def correlation_coefficient(self, vector_a, vector_b):
        """Calculate the correlation coefficient between two vectors."""
        return np.corrcoef(vector_a, vector_b)[0, 1]

    # Projection Operations
    def project_vector_onto_vector(self, vector_a, vector_b):
        """Project vector_a onto vector_b."""
        unit_b = self.normalize_vector(vector_b)
        return self.dot_product(vector_a, unit_b) * unit_b

    # Vector Manipulation and Utility
    def generate_random_vector(self, size):
        """Generate a random vector of specified size."""
        return np.random.rand(size)

    def rotate_vector(self, vector, angle):
        """Rotate a 2D vector by a specified angle in degrees."""
        theta = np.radians(angle)
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        return np.dot(rotation_matrix, vector)

    # Geometric and Spatial Operations
    def distance_between_points(self, point_a, point_b):
        """Calculate the Euclidean distance between two points."""
        return np.linalg.norm(np.subtract(point_a, point_b))

    def point_in_polygon(self, point, polygon):
        """Determine if a point is inside a polygon defined by vertices."""
        path = ConvexHull(polygon)
        return path.find_simplex(point) >= 0

    def area_of_triangle(self, vertex_a, vertex_b, vertex_c):
        """Calculate the area of a triangle using its vertices."""
        ab = self.subtract_vectors(vertex_b, vertex_a)
        ac = self.subtract_vectors(vertex_c, vertex_a)
        return 0.5 * self.compute_vector_magnitude(self.cross_product(ab, ac))

    # Advanced Calculations
    def singular_value_decomposition(self, matrix):
        """Compute the Singular Value Decomposition of a matrix."""
        return np.linalg.svd(matrix)

    def solve_linear_system(self, coefficients, constants):
        """Solve a linear system Ax = b."""
        return np.linalg.solve(coefficients, constants)

    def compute_area_of_polygon(self, vertices):
        """Calculate the area of a polygon using the Shoelace formula."""
        vertices = np.array(vertices)
        return 0.5 * np.abs(np.dot(vertices[:, 0], np.roll(vertices[:, 1], 1)) - np.dot(vertices[:, 1], np.roll(vertices[:, 0], 1)))

    # Utility Functions
    def save_vector_field(self, filename):
        """Save the vector field to a file."""
        np.savetxt(filename, self.vector_field)
        print(f"Vector field saved to '{filename}'.")

    def load_vector_field(self, filename):
        """Load the vector field from a file."""
        self.vector_field = np.loadtxt(filename).tolist()
        print(f"Vector field loaded from '{filename}'.")

    def print_vector_field_info(self):
        """Print details of vectors in the field."""
        print(f"Total vectors in the field: {len(self.vector_field)}")
        for i, vector in enumerate(self.vector_field):
            print(f"Vector {i}: {vector}, Magnitude: {self.compute_vector_magnitude(vector)}")


    def compute_vector_magnitude(self, vector):
        """Compute the magnitude of a vector."""
        return np.linalg.norm(vector)

    def normalize_vector(self, vector):
        """Normalize a vector."""
        magnitude = self.compute_vector_magnitude(vector)
        if magnitude == 0:
            raise ValueError("Cannot normalize the zero vector.")
        return vector / magnitude

    def list_vector_field(self):
        """List all vectors in the vector field."""
        print("Current Vector Field:")
        for i, vector in enumerate(self.vector_field):
            print(f"Vector {i}: {vector}")

    # Vector Operations
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
        """Calculate the cross product of two 3D vectors."""
        return np.cross(vector_a, vector_b)

    def angle_between_vectors(self, vector_a, vector_b):
        """Calculate the angle between two vectors in degrees."""
        dot_product = self.dot_product(vector_a, vector_b)
        magnitudes = self.compute_vector_magnitude(vector_a) * self.compute_vector_magnitude(vector_b)
        return np.degrees(np.arccos(dot_product / magnitudes))

    def scalar_multiply(self, vector, scalar):
        """Multiply a vector by a scalar."""
        return np.multiply(vector, scalar)

    def reflect_vector(self, vector, normal):
        """Reflect a vector across a given normal vector."""
        return vector - 2 * self.dot_product(vector, normal) * normal

    ## Matrix Operations
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

    ## Statistical Operations
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

    ## Geometric Operations
    def distance_between_points(self, point_a, point_b):
        """Calculate the Euclidean distance between two points."""
        return np.linalg.norm(np.subtract(point_a, point_b))

    def point_in_polygon(self, point, polygon):
        """Check if a point is inside a given polygon."""
        from matplotlib.path import Path
        path = Path(polygon)
        return path.contains_point(point)

    ## Projection Operations
    def project_vector_onto_vector(self, vector_a, vector_b):
        """Project vector a onto vector b."""
        unit_b = self.normalize_vector(vector_b)
        return self.dot_product(vector_a, unit_b) * unit_b

    def project_vector_onto_plane(self, vector, normal):
        """Project a vector onto a plane defined by a normal vector."""
        return vector - self.project_vector_onto_vector(vector, normal)

    ## Vector Generation and Manipulation
    def generate_random_vector(self, size):
        """Generate a random vector of a given size."""
        return np.random.rand(size)

    def generate_unit_vector(self, size):
        """Generate a unit vector of a given size."""
        vector = self.generate_random_vector(size)
        return self.normalize_vector(vector)

    def rotate_vector(self, vector, angle):
        """Rotate a 2D vector by a given angle in degrees."""
        theta = np.radians(angle)
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                     [np.sin(theta), np.cos(theta)]])
        return np.dot(rotation_matrix, vector)

    ## Advanced Matrix Operations
    def singular_value_decomposition(self, matrix):
        """Perform Singular Value Decomposition on a matrix."""
        return np.linalg.svd(matrix)

    def solve_linear_system(self, coefficients, constants):
        """Solve a system of linear equations Ax = b."""
        return np.linalg.solve(coefficients, constants)

    ## Utility Functions
    def clear_vector_field(self):
        """Clear the vector field."""
        self.vector_field = []
        print("Vector field cleared.")

    def scale_vector_field(self, scalar):
        """Scale all vectors in the vector field by a scalar."""
        self.vector_field = [self.scalar_multiply(vector, scalar) for vector in self.vector_field]
        print("Vector field scaled successfully.")

    def apply_function_to_vector_field(self, func):
        """Apply a given function to all vectors in the vector field."""
        self.vector_field = [func(vector) for vector in self.vector_field]
        print("Function applied to vector field successfully.")

    def find_closest_vector(self, target_vector):
        """Find the closest vector in the vector field to a given target vector."""
        distances = [self.compute_vector_magnitude(self.subtract_vectors(vector, target_vector)) for vector in self.vector_field]
        closest_index = np.argmin(distances)
        return self.vector_field[closest_index]

    ## More Vector and Matrix Operations
    def concatenate_vectors(self, vector_a, vector_b):
        """Concatenate two vectors."""
        return np.concatenate((vector_a, vector_b))

    def stack_matrices_vertically(self, matrix_a, matrix_b):
        """Stack two matrices vertically."""
        return np.vstack((matrix_a, matrix_b))

    def stack_matrices_horizontally(self, matrix_a, matrix_b):
        """Stack two matrices horizontally."""
        return np.hstack((matrix_a, matrix_b))

    def find_vector_index(self, vector):
        """Find the index of a vector in the vector field."""
        try:
            return self.vector_field.index(vector)
        except ValueError:
            return -1

    def remove_vector(self, vector):
        """Remove a vector from the vector field."""
        index = self.find_vector_index(vector)
        if index != -1:
            del self.vector_field[index]
            print("Vector removed successfully.")
        else:
            print("Vector not found in the field.")

    ## Randomized Operations
    def random_sample_from_vector_field(self, n):
        """Randomly sample n vectors from the vector field."""
        return np.random.choice(self.vector_field, n, replace=False)

    def shuffle_vector_field(self):
        """Shuffle the vectors in the vector field."""
        np.random.shuffle(self.vector_field)
        print("Vector field shuffled successfully.")

    ## Miscellaneous Operations
    def save_vector_field(self, filename):
        """Save the vector field to a file."""
        np.savetxt(filename, self.vector_field)
        print(f"Vector field saved to '{filename}'.")

    def load_vector_field(self, filename):
        """Load the vector field from a file."""
        self.vector_field = np.loadtxt(filename).tolist()
        print(f"Vector field loaded from '{filename}'.")

    def print_vector_field_info(self):
        """Print information about the vector field."""
        print(f"Total vectors in the field: {len(self.vector_field)}")
        for i, vector in enumerate(self.vector_field):
            print(f"Vector {i}: {vector}, Magnitude: {self.compute_vector_magnitude(vector)}")

    ## Transformation Operations
    def apply_transformation(self, transformation_matrix):
        """Apply a transformation matrix to the vector field."""
        self.vector_field = [self.matrix_multiplication(transformation_matrix, np.array(vector).reshape(-1, 1)).flatten().tolist() for vector in self.vector_field]
        print("Transformation applied successfully.")

    ## Additional 144 Methods
    # Vector Operations
    def compute_angle_between_vectors(self, vector_a, vector_b):
        """Calculate the angle between two vectors in radians."""
        dot_product = self.dot_product(vector_a, vector_b)
        magnitudes = self.compute_vector_magnitude(vector_a) * self.compute_vector_magnitude(vector_b)
        return np.arccos(dot_product / magnitudes)

    def is_orthogonal(self, vector_a, vector_b):
        """Check if two vectors are orthogonal."""
        return self.dot_product(vector_a, vector_b) == 0

    def is_parallel(self, vector_a, vector_b):
        """Check if two vectors are parallel."""
        return np.allclose(self.cross_product(vector_a, vector_b), 0)

    def angle_between_vectors_in_radians(self, vector_a, vector_b):
        """Return the angle between two vectors in radians."""
        return self.compute_angle_between_vectors(vector_a, vector_b)

    def vector_projection(self, vector_a, vector_b):
        """Project vector a onto vector b (result is a vector)."""
        return self.project_vector_onto_vector(vector_a, vector_b)

    def distance_from_point_to_line(self, point, line_point1, line_point2):
        """Calculate the distance from a point to a line segment."""
        line_vec = self.subtract_vectors(line_point2, line_point1)
        point_vec = self.subtract_vectors(point, line_point1)
        line_len = self.compute_vector_magnitude(line_vec)
        line_unit_vec = self.normalize_vector(line_vec)
        projection = self.dot_product(point_vec, line_unit_vec)
        return self.compute_vector_magnitude(self.subtract_vectors(point_vec, line_unit_vec * projection))

    def vector_angle_in_degrees(self, vector_a, vector_b):
        """Calculate the angle in degrees between two vectors."""
        return np.degrees(self.angle_between_vectors(vector_a, vector_b))

    def is_unit_vector(self, vector):
        """Check if a vector is a unit vector."""
        return np.isclose(self.compute_vector_magnitude(vector), 1.0)

    def unit_vector(self, vector):
        """Return the unit vector of a given vector."""
        return self.normalize_vector(vector)

    def distance_from_point_to_plane(self, point, plane_point, plane_normal):
        """Calculate the distance from a point to a plane."""
        return abs(self.dot_product(self.subtract_vectors(point, plane_point), self.normalize_vector(plane_normal)))

    def scalar_product(self, vector_a, vector_b):
        """Calculate the scalar product (dot product) of two vectors."""
        return self.dot_product(vector_a, vector_b)

    def area_of_triangle(self, vertex_a, vertex_b, vertex_c):
        """Calculate the area of a triangle given its vertices."""
        ab = self.subtract_vectors(vertex_b, vertex_a)
        ac = self.subtract_vectors(vertex_c, vertex_a)
        return 0.5 * self.compute_vector_magnitude(self.cross_product(ab, ac))

    def area_of_parallelogram(self, vertex_a, vertex_b, vertex_c):
        """Calculate the area of a parallelogram given its vertices."""
        ab = self.subtract_vectors(vertex_b, vertex_a)
        ac = self.subtract_vectors(vertex_c, vertex_a)
        return self.compute_vector_magnitude(self.cross_product(ab, ac))

    def vector_length(self, vector):
        """Return the length of a vector."""
        return self.compute_vector_magnitude(vector)

    def normalize_vectors(self):
        """Normalize all vectors in the vector field."""
        self.vector_field = [self.normalize_vector(vector) for vector in self.vector_field]
        print("All vectors normalized successfully.")

    def create_identity_matrix(self, size):
        """Create an identity matrix of a given size."""
        return np.eye(size)

    def check_matrix_square(self, matrix):
        """Check if a matrix is square."""
        return matrix.shape[0] == matrix.shape[1]

    def flatten_matrix(self, matrix):
        """Flatten a 2D matrix into a 1D array."""
        return matrix.flatten()

    def calculate_sum_of_matrix(self, matrix):
        """Calculate the sum of all elements in a matrix."""
        return np.sum(matrix)

    def calculate_mean_of_matrix(self, matrix):
        """Calculate the mean of all elements in a matrix."""
        return np.mean(matrix)

    def calculate_max_of_matrix(self, matrix):
        """Calculate the maximum value in a matrix."""
        return np.max(matrix)

    def calculate_min_of_matrix(self, matrix):
        """Calculate the minimum value in a matrix."""
        return np.min(matrix)

    def generate_diagonal_matrix(self, diagonal_elements):
        """Generate a diagonal matrix from a list of diagonal elements."""
        return np.diag(diagonal_elements)

    def calculate_trace_of_matrix(self, matrix):
        """Calculate the trace of a matrix."""
        return np.trace(matrix)

    def check_matrix_symmetry(self, matrix):
        """Check if a matrix is symmetric."""
        return np.array_equal(matrix, matrix.T)

    def calculate_eigenvalues(self, matrix):
        """Calculate the eigenvalues of a matrix."""
        return np.linalg.eigvals(matrix)

    def calculate_condition_number(self, matrix):
        """Calculate the condition number of a matrix."""
        return np.linalg.cond(matrix)

    def create_random_matrix(self, rows, cols):
        """Create a random matrix of given dimensions."""
        return np.random.rand(rows, cols)

    def calculate_adjoint_matrix(self, matrix):
        """Calculate the adjoint of a matrix."""
        return np.linalg.inv(matrix).T * np.linalg.det(matrix)

    def is_invertible(self, matrix):
        """Check if a matrix is invertible."""
        return np.linalg.cond(matrix) < 1 / np.finfo(matrix.dtype).eps

    def calculate_symmetric_part(self, matrix):
        """Calculate the symmetric part of a matrix."""
        return 0.5 * (matrix + matrix.T)

    def calculate_skew_symmetric_part(self, matrix):
        """Calculate the skew-symmetric part of a matrix."""
        return 0.5 * (matrix - matrix.T)

    def find_matrix_inverse(self, matrix):
        """Find the inverse of a matrix."""
        return np.linalg.inv(matrix)

    def compute_geometric_mean(self, vector):
        """Calculate the geometric mean of a vector."""
        return np.prod(vector) ** (1 / len(vector))

    def compute_harmonic_mean(self, vector):
        """Calculate the harmonic mean of a vector."""
        return len(vector) / np.sum(1.0 / np.array(vector))

    def generate_random_matrix_within_bounds(self, rows, cols, lower_bound, upper_bound):
        """Generate a random matrix with values within specified bounds."""
        return np.random.uniform(lower_bound, upper_bound, (rows, cols))

    def calculate_covariance_matrix(self, vectors):
        """Calculate the covariance matrix from a list of vectors."""
        return np.cov(np.array(vectors).T)

    def calculate_correlation_matrix(self, vectors):
        """Calculate the correlation matrix from a list of vectors."""
        return np.corrcoef(np.array(vectors).T)

    def create_column_vector(self, elements):
        """Create a column vector from a list of elements."""
        return np.array(elements).reshape(-1, 1)

    def create_row_vector(self, elements):
        """Create a row vector from a list of elements."""
        return np.array(elements).reshape(1, -1)

    def calculate_inner_product(self, vector_a, vector_b):
        """Calculate the inner product of two vectors."""
        return np.inner(vector_a, vector_b)

    def calculate_outer_product(self, vector_a, vector_b):
        """Calculate the outer product of two vectors."""
        return np.outer(vector_a, vector_b)

    def calculate_frobenius_norm(self, matrix):
        """Calculate the Frobenius norm of a matrix."""
        return np.linalg.norm(matrix, 'fro')

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
                                     [np.sin(theta), np.cos(theta)]])
        return self.matrix_multiplication(rotation_matrix, matrix)

    def check_if_matrix_is_stochastic(self, matrix):
        """Check if a matrix is stochastic (rows sum to 1)."""
        return np.allclose(np.sum(matrix, axis=1), 1)

    def calculate_singular_values(self, matrix):
        """Calculate the singular values of a matrix."""
        return np.linalg.svd(matrix, compute_uv=False)

    def check_if_matrix_is_positive_definite(self, matrix):
        """Check if a matrix is positive definite."""
        return np.all(np.linalg.eigvals(matrix) > 0)

    def compute_kronecker_product(self, matrix_a, matrix_b):
        """Compute the Kronecker product of two matrices."""
        return np.kron(matrix_a, matrix_b)

    def compute_hadamard_product(self, matrix_a, matrix_b):
        """Compute the Hadamard product of two matrices."""
        return np.multiply(matrix_a, matrix_b)

    def calculate_cholesky_decomposition(self, matrix):
        """Calculate the Cholesky decomposition of a positive definite matrix."""
        return np.linalg.cholesky(matrix)

    def calculate_rank_deficiency(self, matrix):
        """Calculate the rank deficiency of a matrix."""
        return matrix.shape[0] - self.matrix_rank(matrix)

    def check_if_matrix_is_orthogonal(self, matrix):
        """Check if a matrix is orthogonal."""
        return np.allclose(np.dot(matrix, matrix.T), np.eye(matrix.shape[0]))

    def compute_pseudo_inverse(self, matrix):
        """Compute the pseudo-inverse of a matrix."""
        return np.linalg.pinv(matrix)

    def calculate_gram_schmidt(self, vectors):
        """Perform Gram-Schmidt orthogonalization on a set of vectors."""
        orthogonal_vectors = []
        for vector in vectors:
            for v in orthogonal_vectors:
                vector -= self.project_vector_onto_vector(vector, v)
            orthogonal_vectors.append(vector)
        return np.array(orthogonal_vectors)

    def compute_distance_between_matrices(self, matrix_a, matrix_b):
        """Compute the Frobenius distance between two matrices."""
        return np.linalg.norm(matrix_a - matrix_b, 'fro')

    def calculate_distance_from_point_to_subspace(self, point, subspace_basis):
        """Calculate the distance from a point to a subspace defined by a basis."""
        projection = np.sum([self.project_vector_onto_vector(point, basis) for basis in subspace_basis], axis=0)
        return self.compute_vector_magnitude(self.subtract_vectors(point, projection))

    def calculate_determinant_of_submatrix(self, matrix, rows, cols):
        """Calculate the determinant of a submatrix defined by specific rows and columns."""
        submatrix = matrix[np.ix_(rows, cols)]
        return self.determinant_matrix(submatrix)

    def compute_bilinear_form(self, matrix, vector_a, vector_b):
        """Compute the bilinear form defined by a matrix and two vectors."""
        return self.dot_product(vector_a, self.matrix_multiplication(matrix, vector_b))

    def calculate_intersection_of_lines(self, line1_point1, line1_point2, line2_point1, line2_point2):
        """Calculate the intersection point of two lines defined by two points each."""
        A = np.array([line1_point2 - line1_point1, line2_point2 - line2_point1]).T
        b = line2_point1 - line1_point1
        if np.linalg.det(A) == 0:
            return None  # Lines are parallel
        t = np.linalg.solve(A, b)
        return line1_point1 + t[0] * (line1_point2 - line1_point1)

    def compute_normal_vector_to_plane(self, point1, point2, point3):
        """Compute the normal vector to a plane defined by three points."""
        vector_a = self.subtract_vectors(point2, point1)
        vector_b = self.subtract_vectors(point3, point1)
        return self.cross_product(vector_a, vector_b)

    def check_if_point_is_in_polyhedron(self, point, vertices):
        """Check if a point is inside a polyhedron defined by its vertices."""
        from scipy.spatial import ConvexHull
        hull = ConvexHull(vertices)
        return hull.find_simplex(point) >= 0

    def calculate_volume_of_polyhedron(self, vertices):
        """Calculate the volume of a polyhedron defined by its vertices."""
        from scipy.spatial import ConvexHull
        hull = ConvexHull(vertices)
        return hull.volume

    def calculate_area_of_polygon(self, vertices):
        """Calculate the area of a polygon defined by its vertices."""
        vertices = np.array(vertices)
        return 0.5 * np.abs(np.dot(vertices[:, 0], np.roll(vertices[:, 1], 1)) - np.dot(np.roll(vertices[:, 0], 1), vertices[:, 1]))

    def calculate_barycentric_coordinates(self, point, vertices):
        """Calculate the barycentric coordinates of a point with respect to a triangle defined by its vertices."""
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

    def calculate_centroid_of_polygon(self, vertices):
        """Calculate the centroid of a polygon defined by its vertices."""
        vertices = np.array(vertices)
        x = vertices[:, 0]
        y = vertices[:, 1]
        A = 0.5 * np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))
        C_x = (1 / (6 * A)) * np.dot(x + np.roll(x, 1), np.roll(y, 1) - y)
        C_y = (1 / (6 * A)) * np.dot(y + np.roll(y, 1), x - np.roll(x, 1))
        return np.array([C_x, C_y])

    def calculate_inertia_tensor(self, vertices):
        """Calculate the inertia tensor of a polygon defined by its vertices."""
        inertia_tensor = np.zeros((2, 2))
        vertices = np.array(vertices)
        for i, v in enumerate(vertices):
            next_v = vertices[(i + 1) % len(vertices)]
            cross_product = np.cross(v, next_v)
            inertia_tensor += (cross_product / 2) * (np.dot(v, v) + np.dot(v, next_v) + np.dot(next_v, next_v))
        return inertia_tensor

    def calculate_distance_between_points_and_polyhedron(self, points, vertices):
        """Calculate the distance from a set of points to a polyhedron defined by its vertices."""
        distances = []
        for point in points:
            if self.check_if_point_is_in_polyhedron(point, vertices):
                distances.append(0)  # Point is inside the polyhedron
            else:
                # Calculate the distance to the closest face of the polyhedron
                distances.append(self.distance_from_point_to_plane(point, vertices[0], self.compute_normal_vector_to_plane(vertices[0], vertices[1], vertices[2])))
        return distances

    def calculate_signed_volume_of_polyhedron(self, vertices):
        """Calculate the signed volume of a polyhedron defined by its vertices."""
        volume = 0
        for i in range(len(vertices) - 2):
            volume += np.dot(vertices[i], self.cross_product(vertices[i + 1], vertices[i + 2])) / 6
        return volume

    def compute_area_of_polygon_using_trapezoidal_rule(self, vertices):
        """Calculate the area of a polygon using the trapezoidal rule."""
        vertices = np.array(vertices)
        n = len(vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += (vertices[j][0] + vertices[i][0]) * (vertices[j][1] - vertices[i][1])
        return 0.5 * area

    def calculate_dihedral_angle(self, normal_a, normal_b):
        """Calculate the dihedral angle between two planes defined by their normals."""
        cosine_angle = self.dot_product(normal_a, normal_b) / (self.compute_vector_magnitude(normal_a) * self.compute_vector_magnitude(normal_b))
        return np.arccos(cosine_angle)

    def compute_intersection_of_two_planes(self, normal_a, d_a, normal_b, d_b):
        """Compute the line of intersection of two planes."""
        n1 = normal_a
        n2 = normal_b
        line_direction = self.cross_product(n1, n2)
        if np.allclose(line_direction, 0):
            return None  # Planes are parallel

        # Solve for a point on the line of intersection
        A = np.array([n1, n2]).T
        b = np.array([d_a, d_b])
        line_point = np.linalg.solve(A, b)

        return line_point, line_direction

    def compute_distance_between_point_and_plane(self, point, plane_normal, plane_d):
        """Compute the distance from a point to a plane."""
        return abs(self.dot_product(point, plane_normal) + plane_d) / self.compute_vector_magnitude(plane_normal)

    def check_if_vectors_are_coplanar(self, vector_a, vector_b, vector_c):
        """Check if three vectors are coplanar."""
        return np.isclose(self.dot_product(self.cross_product(vector_a, vector_b), vector_c), 0)

    def calculate_signed_area_of_polygon(self, vertices):
        """Calculate the signed area of a polygon defined by its vertices."""
        vertices = np.array(vertices)
        n = len(vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
        return 0.5 * area

    def calculate_closest_point_on_line_segment(self, point, line_point1, line_point2):
        """Calculate the closest point on a line segment to a given point."""
        line_vec = self.subtract_vectors(line_point2, line_point1)
        t = self.dot_product(subtract_vectors(point, line_point1), line_vec) / self.dot_product(line_vec, line_vec)
        if t < 0:
            return line_point1
        elif t > 1:
            return line_point2
        else:
            return line_point1 + t * line_vec

    def compute_spherical_coordinates(self, point):
        """Convert Cartesian coordinates to spherical coordinates."""
        r = self.compute_vector_magnitude(point)
        theta = np.arccos(point[2] / r)  # Polar angle
        phi = np.arctan2(point[1], point[0])  # Azimuthal angle
        return np.array([r, theta, phi])

    def compute_cartesian_coordinates(self, spherical_coordinates):
        """Convert spherical coordinates to Cartesian coordinates."""
        r, theta, phi = spherical_coordinates
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return np.array([x, y, z])

    def calculate_area_of_circle(self, radius):
        """Calculate the area of a circle given its radius."""
        return np.pi * radius ** 2

    def calculate_circumference_of_circle(self, radius):
        """Calculate the circumference of a circle given its radius."""
        return 2 * np.pi * radius

    def calculate_area_of_ellipse(self, semi_major_axis, semi_minor_axis):
        """Calculate the area of an ellipse given its semi-major and semi-minor axes."""
        return np.pi * semi_major_axis * semi_minor_axis

    def calculate_area_of_sector(self, radius, angle):
        """Calculate the area of a sector given its radius and angle in radians."""
        return 0.5 * radius ** 2 * angle

    def calculate_perimeter_of_ellipse(self, semi_major_axis, semi_minor_axis):
        """Calculate the perimeter of an ellipse using Ramanujan's approximation."""
        return np.pi * (3 * (semi_major_axis + semi_minor_axis) - np.sqrt((3 * semi_major_axis + semi_minor_axis) * (semi_major_axis + 3 * semi_minor_axis)))

    def calculate_volume_of_cylinder(self, radius, height):
        """Calculate the volume of a cylinder given its radius and height."""
        return self.calculate_area_of_circle(radius) * height

    def calculate_surface_area_of_cylinder(self, radius, height):
        """Calculate the surface area of a cylinder given its radius and height."""
        return 2 * self.calculate_area_of_circle(radius) + 2 * np.pi * radius * height

    def calculate_volume_of_cone(self, radius, height):
        """Calculate the volume of a cone given its radius and height."""
        return (1 / 3) * self.calculate_area_of_circle(radius) * height

    def calculate_surface_area_of_cone(self, radius, slant_height):
        """Calculate the surface area of a cone given its radius and slant height."""
        return self.calculate_area_of_circle(radius) + np.pi * radius * slant_height

    def calculate_volume_of_sphere(self, radius):
        """Calculate the volume of a sphere given its radius."""
        return (4 / 3) * np.pi * radius ** 3

    def calculate_surface_area_of_sphere(self, radius):
        """Calculate the surface area of a sphere given its radius."""
        return 4 * self.calculate_area_of_circle(radius)

    def calculate_volume_of_torus(self, major_radius, minor_radius):
        """Calculate the volume of a torus given its major and minor radii."""
        return (2 * np.pi * minor_radius) * (np.pi * major_radius ** 2)

    def calculate_surface_area_of_torus(self, major_radius, minor_radius):
        """Calculate the surface area of a torus given its major and minor radii."""
        return (2 * np.pi * minor_radius) * (2 * np.pi * major_radius)

    def calculate_area_of_triangle_from_coordinates(self, vertex_a, vertex_b, vertex_c):
        """Calculate the area of a triangle given its vertices."""
        return 0.5 * np.abs((vertex_a[0] * (vertex_b[1] - vertex_c[1]) + 
                              vertex_b[0] * (vertex_c[1] - vertex_a[1]) + 
                              vertex_c[0] * (vertex_a[1] - vertex_b[1])))

    def calculate_volume_of_prism(self, base_area, height):
        """Calculate the volume of a prism given its base area and height."""
        return base_area * height

    def calculate_surface_area_of_prism(self, base_area, perimeter, height):
        """Calculate the surface area of a prism given its base area, perimeter, and height."""
        return 2 * base_area + perimeter * height

    def calculate_surface_area_of_pyramid(self, base_area, slant_height, base_perimeter):
        """Calculate the surface area of a pyramid given its base area, slant height, and base perimeter."""
        return base_area + (base_perimeter * slant_height) / 2

    def calculate_volume_of_pyramid(self, base_area, height):
        """Calculate the volume of a pyramid given its base area and height."""
        return (1 / 3) * base_area * height

    def calculate_moment_of_inertia_of_circle(self, radius):
        """Calculate the moment of inertia of a circle given its radius."""
        return (1 / 2) * self.calculate_area_of_circle(radius) * radius ** 2

    def calculate_moment_of_inertia_of_rectangle(self, width, height):
        """Calculate the moment of inertia of a rectangle given its width and height."""
        return (1 / 12) * width * height ** 3

    def calculate_moment_of_inertia_of_triangle(self, base, height):
        """Calculate the moment of inertia of a triangle given its base and height."""
        return (1 / 36) * base * height ** 3

    def calculate_moment_of_inertia_of_solid_sphere(self, radius):
        """Calculate the moment of inertia of a solid sphere given its radius."""
        return (2 / 5) * self.calculate_volume_of_sphere(radius) * radius ** 2

    def calculate_moment_of_inertia_of_cylinder(self, radius, height):
        """Calculate the moment of inertia of a cylinder given its radius and height."""
        return (1 / 12) * self.calculate_volume_of_cylinder(radius, height) * (3 * radius ** 2 + height ** 2)

    def calculate_moment_of_inertia_of_pyramid(self, base_area, height):
        """Calculate the moment of inertia of a pyramid given its base area and height."""
        return (1 / 10) * base_area * height ** 2

    def calculate_center_of_mass_of_polygon(self, vertices):
        """Calculate the center of mass of a polygon defined by its vertices."""
        area = self.calculate_area_of_polygon(vertices)
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

    def calculate_volume_of_frustum(self, base_area1, base_area2, height):
        """Calculate the volume of a frustum given the areas of its bases and its height."""
        return (1 / 3) * height * (base_area1 + base_area2 + np.sqrt(base_area1 * base_area2))

    def calculate_surface_area_of_frustum(self, base_area1, base_area2, slant_height):
        """Calculate the surface area of a frustum given the areas of its bases and its slant height."""
        return base_area1 + base_area2 + (base_area1 + base_area2) * slant_height

    def calculate_surface_area_of_ellipsoid(self, semi_major_axis, semi_minor_axis):
        """Approximate the surface area of an ellipsoid using Knud Thomsen's formula."""
        p = 1.6075  # Exponent in the formula
        a = semi_major_axis
        b = semi_minor_axis
        return 4 * np.pi * ((a ** p * b ** p) ** (1 / p))

    def calculate_volume_of_ellipsoid(self, semi_major_axis, semi_minor_axis):
        """Calculate the volume of an ellipsoid given its semi-major and semi-minor axes."""
        return (4 / 3) * np.pi * semi_major_axis * semi_minor_axis ** 2

    def calculate_volume_of_tetrahedron(self, vertices):
        """Calculate the volume of a tetrahedron defined by its vertices."""
        return abs(np.linalg.det(np.hstack((vertices, np.ones((4, 1))))) / 6)

    def calculate_area_of_tetrahedron(self, vertices):
        """Calculate the surface area of a tetrahedron defined by its vertices."""
        return sum(self.calculate_area_of_triangle_from_coordinates(vertices[i], vertices[j], vertices[k])
                   for i in range(4) for j in range(i + 1, 4) for k in range(j + 1, 4))

    def calculate_distance_between_tetrahedron_and_point(self, vertices, point):
        """Calculate the distance between a point and a tetrahedron defined by its vertices."""
        if self.check_if_point_is_in_polyhedron(point, vertices):
            return 0  # Point is inside the tetrahedron
        else:
            return min(self.distance_from_point_to_plane(point, vertices[i], self.compute_normal_vector_to_plane(vertices[i], vertices[j], vertices[k]))
                       for i in range(4) for j in range(i + 1, 4) for k in range(j + 1, 4))

    def calculate_volume_of_polygonal_prism(self, vertices, height):
        """Calculate the volume of a polygonal prism given the vertices of its base and its height."""
        base_area = self.calculate_area_of_polygon(vertices)
        return base_area * height

    def calculate_surface_area_of_polygonal_prism(self, vertices, height):
        """Calculate the surface area of a polygonal prism given the vertices of its base and its height."""
        base_area = self.calculate_area_of_polygon(vertices)
        perimeter = np.sum([self.compute_distance_between_points_and_polyhedron(vertices[i], vertices[(i + 1) % len(vertices)]) 
                             for i in range(len(vertices))])
        return 2 * base_area + perimeter * height

    def calculate_volume_of_spherical_cap(self, radius, height):
        """Calculate the volume of a spherical cap given its radius and height."""
        return (1 / 3) * np.pi * height ** 2 * (3 * radius - height)

    def calculate_surface_area_of_spherical_cap(self, radius, height):
        """Calculate the surface area of a spherical cap given its radius and height."""
        return 2 * np.pi * radius * height

    def calculate_spherical_coordinates_of_polygon(self, vertices):
        """Convert the vertices of a polygon to spherical coordinates."""
        return np.array([self.compute_spherical_coordinates(vertex) for vertex in vertices])

    def calculate_cartesian_coordinates_of_polygon(self, spherical_coordinates):
        """Convert the spherical coordinates of a polygon to Cartesian coordinates."""
        return np.array([self.compute_cartesian_coordinates(spherical_coordinate) for spherical_coordinate in spherical_coordinates])

    def calculate_volume_of_polygonal_frustum(self, base_area1, base_area2, height):
        """Calculate the volume of a polygonal frustum given the areas of its bases and its height."""
        return (1 / 3) * height * (base_area1 + base_area2 + np.sqrt(base_area1 * base_area2))

    def calculate_surface_area_of_polygonal_frustum(self, base_area1, base_area2, slant_height):
        """Calculate the surface area of a polygonal frustum given the areas of its bases and its slant height."""
        return base_area1 + base_area2 + (base_area1 + base_area2) * slant_height

    def calculate_moments_of_inertia_of_polygonal_shape(self, vertices):
        """Calculate the moments of inertia of a polygonal shape defined by its vertices."""
        I_x = 0
        I_y = 0
        A = self.calculate_area_of_polygon(vertices)
        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            I_x += (vertices[i][1] ** 2 + vertices[j][1] ** 2) * (vertices[j][0] - vertices[i][0])
            I_y += (vertices[i][0] ** 2 + vertices[j][0] ** 2) * (vertices[j][1] - vertices[i][1])
        return (1 / 12) * A, (1 / 12) * A

    def calculate_polar_coordinates(self, point):
        """Convert Cartesian coordinates to polar coordinates."""
        r = np.sqrt(point[0] ** 2 + point[1] ** 2)
        theta = np.arctan2(point[1], point[0])
        return np.array([r, theta])

    def calculate_cartesian_coordinates_from_polar(self, polar_coordinates):
        """Convert polar coordinates to Cartesian coordinates."""
        r, theta = polar_coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.array([x, y])
