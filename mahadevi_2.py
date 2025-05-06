import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.path import Path

class Mahadevi:
    def __init__(self):
        self.vector_field = []

    def set_vector_field(self, vectors):
        self.vector_field = vectors

    def list_vector_field(self):
        for i, v in enumerate(self.vector_field):
            print(f"Vector {i}: {v}")

    def add_vectors(self, a, b): return np.add(a, b)
    def subtract_vectors(self, a, b): return np.subtract(a, b)
    def dot_product(self, a, b): return np.dot(a, b)
    def cross_product(self, a, b): return np.cross(a, b)
    def scalar_multiply(self, v, s): return np.multiply(v, s)
    def compute_vector_magnitude(self, v): return np.linalg.norm(v)
    def normalize_vector(self, v):
        mag = self.compute_vector_magnitude(v)
        if mag == 0: raise ValueError("Zero vector")
        return v / mag
    def angle_between_vectors(self, a, b): 
        return np.degrees(np.arccos(self.dot_product(a, b) / (self.compute_vector_magnitude(a) * self.compute_vector_magnitude(b))))
    def project_vector_onto_vector(self, a, b):
        unit_b = self.normalize_vector(b)
        return self.dot_product(a, unit_b) * unit_b
    def reflect_vector(self, v, normal):
        return v - 2 * self.dot_product(v, normal) * normal
    def transpose_matrix(self, m): return np.transpose(m)
    def matrix_multiplication(self, a, b): return np.matmul(a, b)
    def inverse_matrix(self, m): return np.linalg.inv(m)
    def determinant_matrix(self, m): return np.linalg.det(m)
    def eigenvalues_and_vectors(self, m): return np.linalg.eig(m)
    def matrix_rank(self, m): return np.linalg.matrix_rank(m)
    def mean_vector(self, v): return np.mean(v)
    def median_vector(self, v): return np.median(v)
    def variance_vector(self, v): return np.var(v)
    def standard_deviation_vector(self, v): return np.std(v)
    def correlation_coefficient(self, a, b): return np.corrcoef(a, b)[0,1]
    def distance_between_points(self, a, b): return np.linalg.norm(np.subtract(a, b))
    def point_in_polygon(self, point, polygon): return Path(polygon).contains_point(point)
    def project_vector_onto_plane(self, v, normal): return v - self.project_vector_onto_vector(v, normal)
    def generate_random_vector(self, size): return np.random.rand(size)
    def rotate_vector(self, v, angle_deg):
        theta = np.radians(angle_deg)
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        return np.dot(rot, v)
    def singular_value_decomposition(self, m): return np.linalg.svd(m)
    def solve_linear_system(self, A, b): return np.linalg.solve(A, b)
    def compute_area_of_polygon(self, vertices):
        v = np.array(vertices)
        return 0.5 * np.abs(np.dot(v[:, 0], np.roll(v[:, 1], 1)) - np.dot(v[:, 1], np.roll(v[:, 0], 1)))
    def clear_vector_field(self): self.vector_field = []
    def scale_vector_field(self, scalar): self.vector_field = [self.scalar_multiply(v, scalar) for v in self.vector_field]
    def apply_function_to_vector_field(self, func): self.vector_field = [func(v) for v in self.vector_field]
    def find_closest_vector(self, target): return min(self.vector_field, key=lambda v: self.compute_vector_magnitude(self.subtract_vectors(v, target)))
    def concatenate_vectors(self, a, b): return np.concatenate((a, b))
    def stack_matrices_vertically(self, a, b): return np.vstack((a, b))
    def stack_matrices_horizontally(self, a, b): return np.hstack((a, b))
    def find_vector_index(self, vector): 
        try: return self.vector_field.index(vector)
        except ValueError: return -1
    def remove_vector(self, vector): 
        idx = self.find_vector_index(vector)
        if idx != -1: del self.vector_field[idx]
    def random_sample_from_vector_field(self, n): return np.random.choice(self.vector_field, n, replace=False)
    def shuffle_vector_field(self): np.random.shuffle(self.vector_field)
    def save_vector_field(self, fname): np.savetxt(fname, self.vector_field)
    def load_vector_field(self, fname): self.vector_field = np.loadtxt(fname).tolist()
    def apply_transformation(self, T):
        self.vector_field = [self.matrix_multiplication(T, np.array(v).reshape(-1, 1)).flatten().tolist() for v in self.vector_field]
    def create_identity_matrix(self, size): return np.eye(size)
    def check_matrix_square(self, m): return m.shape[0] == m.shape[1]
    def flatten_matrix(self, m): return m.flatten()
    def generate_diagonal_matrix(self, elems): return np.diag(elems)
    def check_matrix_symmetry(self, m): return np.allclose(m, m.T)
    def is_invertible(self, m): return np.linalg.cond(m) < 1 / np.finfo(m.dtype).eps
    def calculate_trace_of_matrix(self, m): return np.trace(m)
    def calculate_covariance_matrix(self, v): return np.cov(np.array(v).T)
    def calculate_correlation_matrix(self, v): return np.corrcoef(np.array(v).T)
    def create_column_vector(self, elems): return np.array(elems).reshape(-1, 1)
    def create_row_vector(self, elems): return np.array(elems).reshape(1, -1)
    def compute_area_of_triangle(self, a, b, c): return 0.5 * self.compute_vector_magnitude(self.cross_product(self.subtract_vectors(b, a), self.subtract_vectors(c, a)))
    def distance_from_point_to_plane(self, p, plane_p, plane_n): return abs(self.dot_product(self.subtract_vectors(p, plane_p), self.normalize_vector(plane_n)))

    # More methods exist – truncated for brevity