import numpy as np
import random
import time

def initial_tour(n):
    tour = list(range(n))
    random.shuffle(tour)
    tour.append(tour[0])
    return tour

def tour_cost(tour, matrix):
    cost = 0
    for i in range(len(tour) - 1):
        cost += matrix[tour[i]][tour[i + 1]]
    return cost

def swap_move(tour):
    tour_copy = tour[:-1].copy()
    i, j = random.sample(range(len(tour_copy)), 2)
    tour_copy[i], tour_copy[j] = tour_copy[j], tour_copy[i]
    tour_copy.append(tour_copy[0])
    return tour_copy

def simulated_annealing(matrix_file, initial_temp=10000, min_temp=1, alpha=0.003):
    matrix = np.load(matrix_file)
    n = len(matrix)
    current_tour = initial_tour(n)
    current_cost = tour_cost(current_tour, matrix)
    
    start_time = time.time()
    temp = initial_temp
    iterations = 0
    
    while temp > min_temp:
        new_tour = swap_move(current_tour)
        new_cost = tour_cost(new_tour, matrix)
        delta = new_cost - current_cost
        
        if delta < 0 or random.random() < np.exp(-delta / temp):
            current_tour = new_tour
            current_cost = new_cost
        
        temp *= (1 - alpha)
        iterations += 1
    
    runtime = time.time() - start_time
    return current_tour, current_cost, runtime, iterations

def solve_all_instances():
    # Define the instances to solve
    instances = [
        "ulysses22_distance_matrix.npy",
        "att48_distance_matrix.npy", 
        "ch150_distance_matrix.npy"
    ]
    
    # Store results for comparison
    results = {}
    
    print("=" * 70)
    print("TRAVELING SALESMAN PROBLEM - SIMULATED ANNEALING SOLVER")
    print("=" * 70)
    print()
    
    for instance in instances:
        try:
            print(f"Solving instance: {instance}")
            print("-" * 50)
            
            # Run simulated annealing
            tour, cost, runtime, iterations = simulated_annealing(instance)
            
            # Store results
            results[instance] = {
                'tour': tour,
                'cost': cost,
                'runtime': runtime,
                'iterations': iterations,
                'cities': len(tour) - 1
            }
            
            # Display results
            print(f"Instance: {instance}")
            print(f"Number of cities: {len(tour) - 1}")
            print(f"Best tour cost: {cost:.2f}")
            print(f"Runtime: {runtime:.2f} seconds")
            print(f"Iterations: {iterations:,}")
            print(f"Tour: {tour[:10]}{'...' if len(tour) > 11 else tour[10:]}")
            print()
            
        except FileNotFoundError:
            print(f"Error: Could not find file '{instance}'")
            print("Please ensure the file exists in the current directory.")
            print()
        except Exception as e:
            print(f"Error processing {instance}: {str(e)}")
            print()
    
    # Summary comparison
    if results:
        print("=" * 70)
        print("SUMMARY COMPARISON")
        print("=" * 70)
        print(f"{'Instance':<35} {'Cities':<8} {'Cost':<12} {'Runtime (s)':<12} {'Iterations':<12}")
        print("-" * 70)
        
        for instance, data in results.items():
            instance_name = instance.replace('_distance_matrix.npy', '')
            print(f"{instance_name:<35} {data['cities']:<8} {data['cost']:<12.2f} {data['runtime']:<12.2f} {data['iterations']:<12,}")
        
        print()
        
        # Find best performance metrics
        if len(results) > 1:
            fastest_instance = min(results.items(), key=lambda x: x[1]['runtime'])
            most_efficient = min(results.items(), key=lambda x: x[1]['cost'] / x[1]['cities'])
            
            print("PERFORMANCE HIGHLIGHTS:")
            print(f"• Fastest solve: {fastest_instance[0].replace('_distance_matrix.npy', '')} "
                  f"({fastest_instance[1]['runtime']:.2f}s)")
            print(f"• Most efficient (cost/city): {most_efficient[0].replace('_distance_matrix.npy', '')} "
                  f"({most_efficient[1]['cost']/most_efficient[1]['cities']:.2f})")
    
    return results

def run_multiple_trials(instance, num_trials=5):
    """Run multiple trials for better statistical analysis"""
    print(f"\nRunning {num_trials} trials for {instance}...")
    
    costs = []
    runtimes = []
    
    for trial in range(num_trials):
        _, cost, runtime, _ = simulated_annealing(instance)
        costs.append(cost)
        runtimes.append(runtime)
        print(f"Trial {trial + 1}: Cost = {cost:.2f}, Runtime = {runtime:.2f}s")
    
    print(f"\nStatistics for {instance}:")
    print(f"Best cost: {min(costs):.2f}")
    print(f"Average cost: {np.mean(costs):.2f}")
    print(f"Worst cost: {max(costs):.2f}")
    print(f"Standard deviation: {np.std(costs):.2f}")
    print(f"Average runtime: {np.mean(runtimes):.2f}s")

if __name__ == "__main__":
    # Set random seed for reproducibility (optional)
    random.seed(42)
    np.random.seed(42)
    
    # Solve all instances
    results = solve_all_instances()
    
    # Optional: Run multiple trials for statistical analysis
    # Uncomment the lines below to run multiple trials for each instance
    # print("\n" + "=" * 70)
    # print("STATISTICAL ANALYSIS (Multiple Trials)")
    # print("=" * 70)
    # 
    # for instance in ["ulysses22_distance_matrix.npy", "att48_distance_matrix.npy", "ch150_distance_matrix.npy"]:
    #     try:
    #         run_multiple_trials(instance, num_trials=3)
    #         print()
    #     except FileNotFoundError:
    #         print(f"Skipping {instance} - file not found")
    #         continue