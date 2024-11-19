import os
import ast
import re
import pandas as pd
import numpy as np
from typing import List, Dict

def get_code_files(root_dir, extensions=[".py"]):
    """Walk through a directory and return a list of code files."""
    code_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))
    return code_files

def extract_functions(file_path):
    """Extract functions, their docstrings, and code snippets from a Python file."""
    functions = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            tree = ast.parse("".join(lines))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                docstring = ast.get_docstring(node)
                start_line = node.lineno - 1  # Convert to 0-based index
                end_line = max(getattr(node, "end_lineno", start_line), start_line)
                code_snippet = "".join(lines[start_line:end_line])
                functions.append({
                    "name": func_name,
                    "docstring": docstring,
                    "start_line": start_line + 1,  # Convert back to 1-based index for CSV
                    "end_line": end_line,
                    "code_snippet": code_snippet.strip()
                })
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return functions

def extract_comments(file_path):
    """Extract comments and their surrounding code snippets from a Python file."""
    comments = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines, start=1):
                comment_match = re.search(r"#(.+)", line)
                if comment_match:
                    # Capture the surrounding code snippet for context
                    snippet_start = max(0, line_num - 3)  # 3 lines before the comment
                    snippet_end = min(len(lines), line_num + 2)  # 2 lines after the comment
                    code_snippet = "".join(lines[snippet_start:snippet_end])
                    comments.append({
                        "line": line_num,
                        "comment": comment_match.group(1).strip(),
                        "code_snippet": code_snippet.strip()
                    })
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return comments

def schrodinger_transport(data: List[str]) -> List[float]:
    """Apply Quantum Schrödinger Transport to accelerate feature extraction."""
    # Simplified quantum transport simulation using wave function-like modeling
    transport_results = []
    for snippet in data:
        wave_packet = np.sin(len(snippet)) * np.exp(-np.array([ord(c) for c in snippet]) / len(snippet))
        transport_results.append(np.sum(wave_packet))
    return transport_results

def juxtapose_features(feature_set_1: List[float], feature_set_2: List[float]) -> List[float]:
    """Juxtapose two feature sets to form a composite representation."""
    return [a + b for a, b in zip(feature_set_1, feature_set_2)]

def create_dataset(root_directory):
    """Create a dataset from Python files in a directory."""
    code_files = get_code_files(root_directory)
    print(f"Found {len(code_files)} Python files.")

    dataset = []

    for file in code_files:
        # Extract functions
        functions = extract_functions(file)
        for func in functions:
            dataset.append({
                "file_path": file,
                "type": "function",
                "name": func["name"],
                "label": "function",
                "docstring": func["docstring"],
                "start_line": func["start_line"],
                "end_line": func["end_line"],
                "comment": None,
                "code": func["code_snippet"].strip(),
            })

        # Extract comments
        comments = extract_comments(file)
        for comment in comments:
            dataset.append({
                "file_path": file,
                "type": "comment",
                "name": None,
                "label": "comment",
                "docstring": None,
                "start_line": comment["line"],
                "end_line": comment["line"],
                "comment": comment["comment"],
                "code": comment["code_snippet"].strip(),
            })

    # Convert to DataFrame
    df = pd.DataFrame(dataset)

    # Ensure required columns exist
    required_columns = ["name", "code", "label", "start_line", "end_line"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = None  # Add missing columns with default values

    # Ensure `start_line` is filled with defaults
    df["start_line"] = df["start_line"].fillna(0).astype(int)

    # Apply Quantum Schrödinger Transport to accelerate feature extraction
    df["quantum_transport"] = schrodinger_transport(df["code"].fillna("").tolist())

    # Generate juxtaposed features combining transport and start_line
    juxt_features = juxtapose_features(
        df["quantum_transport"].fillna(0).tolist(),
        df["start_line"].fillna(0).astype(float).tolist()
    )
    df["juxt_features"] = juxt_features

    # Add placeholders for optional columns
    optional_columns = ["embedding", "dependencies"]
    for col in optional_columns:
        if col not in df.columns:
            df[col] = None

    return df


if __name__ == "__main__":
    # Set the root directory to scan
    root_directory = r"C:\Users\round\OneDrive\Desktop\SteelOx"

    # Create the dataset
    df = create_dataset(root_directory)

    # Save to CSV
    output_path = "code_dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
