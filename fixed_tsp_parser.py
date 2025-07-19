import xml.etree.ElementTree as ET
import numpy as np
import os

def parse_tsp_xml(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    graph = {}
    vertex_elements = root.findall('.//vertex')
    
    for vertex_idx, vertex_elem in enumerate(vertex_elements):
        graph[vertex_idx] = []
        edge_elements = vertex_elem.findall('.//edge')
        for edge_elem in edge_elements:
            try:
                neighbor = int(edge_elem.text.strip())
                cost = float(edge_elem.get('cost'))
                graph[vertex_idx].append((neighbor, cost))
            except (AttributeError, ValueError, TypeError):
                continue
    
    return graph

def create_distance_matrix(graph):
    """Create distance matrix from graph dictionary."""
    if not graph:
        raise ValueError("Graph is empty - cannot create distance matrix")
    
    num_vertices = len(graph)
    distance_matrix = np.full((num_vertices, num_vertices), np.inf, dtype=np.float64)
    np.fill_diagonal(distance_matrix, 0.0)
    
    for vertex_idx, edges in graph.items():
        for neighbor, cost in edges:
            distance_matrix[vertex_idx][neighbor] = cost
    
    return distance_matrix

def save_distance_matrix(distance_matrix, output_path):
    """Save distance matrix as .npy file."""
    np.save(output_path, distance_matrix)
    print(f"Distance matrix saved to: {output_path}")
    print(f"Matrix shape: {distance_matrix.shape}")

def print_graph_summary(graph):
    num_vertices = len(graph)
    total_edges = sum(len(edges) for edges in graph.values())
    print(f"Number of vertices: {num_vertices}")
    print(f"Total edges parsed: {total_edges}")

if __name__ == "__main__":
    file_path = 'att48.xml'  # Replace with your XML file path
    
    # Generate output filename
    base_name = os.path.splitext(file_path)[0]
    output_file = f"{base_name}_distance_matrix.npy"
    
    try:
        print(f"Parsing XML file: {file_path}")
        graph = parse_tsp_xml(file_path)
        print_graph_summary(graph)
        
        print("\nCreating distance matrix...")
        distance_matrix = create_distance_matrix(graph)
        
        print(f"Saving distance matrix...")
        save_distance_matrix(distance_matrix, output_file)
        
        print(f"\nComplete! Load with: np.load('{output_file}')")
        
    except Exception as e:
        print(f"Error: {e}")