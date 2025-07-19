from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from google.protobuf import duration_pb2
import numpy as np
import time

def solve_tsp_ortools(matrix_file, instance_name, time_limit_seconds=30):
    try:
        # Load distance matrix
        matrix = np.load(matrix_file)
        num_vertices = len(matrix)
        
        # Adjust time limit based on instance size
        if num_vertices > 100:  # Large instances like ch150
            time_limit_seconds = 60  # More time for larger instances
        
        # Create TSP solver
        manager = pywrapcp.RoutingIndexManager(num_vertices, 1, 0)
        routing = pywrapcp.RoutingModel(manager)
        
        # Define the distance callback
        def distance_callback(from_index, to_index):
            # Convert indices to node numbers
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(matrix[from_node][to_node])
        
        # Register the callback
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        # Set search parameters with time limit
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        # Set time limit using Duration object
        search_parameters.time_limit.CopyFrom(
            duration_pb2.Duration(seconds=time_limit_seconds)
        )
        # Optional: Set the search strategy (can improve performance)
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        
        # Solve
        start_time = time.time()
        solution = routing.SolveWithParameters(search_parameters)
        end_time = time.time()
        
        if solution:
            total_cost = solution.ObjectiveValue()
            tour = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                tour.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            tour.append(manager.IndexToNode(index))  # Return to start
            runtime = end_time - start_time
            return tour, total_cost, runtime
        
        runtime = end_time - start_time
        return None, float('inf'), runtime
        
    except Exception as e:
        print(f"Error solving {matrix_file}: {e}")
        return None, float('inf'), 0

if __name__ == "__main__":
    # List of instances with optimal distances
    instances = [
        ('ulysses22', 'ulysses22_distance_matrix.npy', 7013),
        ('att48', 'att48_distance_matrix.npy', 10628),
        ('ch150', 'ch150_distance_matrix.npy', 6528)
    ]
    
    # Solve each instance
    for instance_name, matrix_file, optimal_distance in instances:
        tour, cost, runtime = solve_tsp_ortools(matrix_file, instance_name)
        
        if tour and cost != float('inf'):
            print(f"{instance_name}: Cost={cost:.2f}, Gap={((cost - optimal_distance) / optimal_distance * 100):.2f}%, Time={runtime:.2f}s")
        else:
            if runtime >= 30:  # Check if it was a timeout
                print(f"{instance_name}: TIMEOUT (>{runtime:.1f}s)")
            else:
                print(f"{instance_name}: FAILED")