"""
Main Monopoly Monte Carlo Simulation
Runs simulations and exports results to CSV.
"""

import csv
import time
from utils.board import BOARD_SPACES, COLOR_GROUPS, get_space_name, get_color_group
from utils.simulation import MonopolySimulation, run_both_strategies


def save_probabilities_to_csv(probabilities, filename):
    """
    Save landing probabilities to a CSV file.
    
    Args:
        probabilities: Array of probabilities for each space (0-39)
        filename: Name of the CSV file to create
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Space', 'Space Name', 'Probability'])
        
        for space_num in range(40):
            space_name = get_space_name(space_num)
            probability = probabilities[space_num]
            writer.writerow([space_num, space_name, f"{probability:.6f}"])
    
    print(f"Saved probabilities to {filename}")


def main():
    """Run simulations and export results."""
    print("=" * 70)
    print("MONOPOLY LANDING PROBABILITIES - MONTE CARLO SIMULATION")
    print("=" * 70)
    
    start_time = time.time()
    
    # Run simulations for both jail strategies
    probs_A, probs_B = run_both_strategies(num_iterations=100_000, turns_per_iteration=10_000)
    
    # Save results to CSV files
    save_probabilities_to_csv(probs_A, 'stratA_probs.csv')
    save_probabilities_to_csv(probs_B, 'stratB_probs.csv')
    
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 70)
    print(f"Simulation complete! Total time: {elapsed_time:.2f} seconds")
    print("=" * 70)
    
    # Display top 10 most visited spaces for each strategy
    print("\nTop 10 Most Visited Spaces:")
    print("\nStrategy A (Stay in Jail):")
    ranked_A = sorted([(i, probs_A[i]) for i in range(40)], key=lambda x: x[1], reverse=True)
    for rank, (space, prob) in enumerate(ranked_A[:10], 1):
        print(f"{rank:2d}. {get_space_name(space):25s} - {prob:.4%}")
    
    print("\nStrategy B (Leave Jail Immediately):")
    ranked_B = sorted([(i, probs_B[i]) for i in range(40)], key=lambda x: x[1], reverse=True)
    for rank, (space, prob) in enumerate(ranked_B[:10], 1):
        print(f"{rank:2d}. {get_space_name(space):25s} - {prob:.4%}")


if __name__ == "__main__":
    main()

