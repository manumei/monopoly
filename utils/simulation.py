"""
Monte Carlo Simulation Engine
Runs multiple iterations to calculate long-term landing probabilities.
"""

import numpy as np
from tqdm import tqdm
from player import Player
from cards import create_decks


class MonopolySimulation:
    """Runs Monte Carlo simulation for Monopoly board probabilities."""
    
    def __init__(self, num_iterations=1_000_000, turns_per_iteration=10_000):
        """
        Initialize simulation parameters.
        
        Args:
            num_iterations: Number of independent simulations to run
            turns_per_iteration: Number of turns per simulation (to reach equilibrium)
        """
        self.num_iterations = num_iterations
        self.turns_per_iteration = turns_per_iteration
        self.landing_counts = None
    
    def run_simulation(self, jail_strategy='A'):
        """
        Run the simulation for a specific jail strategy.
        
        Args:
            jail_strategy: 'A' (stay in jail) or 'B' (leave immediately)
        
        Returns:
            numpy.ndarray: Count of landings on each space (0-39)
        """
        landing_counts = np.zeros(40, dtype=np.int64)
        
        print(f"\nRunning simulation with Jail Strategy {jail_strategy}...")
        print(f"Iterations: {self.num_iterations:,}, Turns per iteration: {self.turns_per_iteration:,}")
        
        # Use tqdm for progress bar
        for iteration in tqdm(range(self.num_iterations), 
                              desc=f"Strategy {jail_strategy}",
                              unit="iter",
                              colour="green"):
            # Create new player and decks for this iteration
            player = Player(jail_strategy=jail_strategy)
            chance_deck, community_chest_deck = create_decks()
            
            # Run turns for this iteration
            for turn in range(self.turns_per_iteration):
                final_position = player.take_turn(chance_deck, community_chest_deck)
                landing_counts[final_position] += 1
        
        self.landing_counts = landing_counts
        return landing_counts
    
    def calculate_probabilities(self, landing_counts):
        """
        Convert landing counts to probabilities.
        
        Args:
            landing_counts: Array of landing counts for each space
        
        Returns:
            numpy.ndarray: Probability distribution (sums to 1.0)
        """
        total_landings = np.sum(landing_counts)
        probabilities = landing_counts / total_landings
        return probabilities
    
    def get_ranked_spaces(self, probabilities):
        """
        Get spaces ranked from most to least visited.
        
        Args:
            probabilities: Array of probabilities for each space
        
        Returns:
            list: List of (space_number, probability) tuples, sorted by probability
        """
        ranked = [(i, probabilities[i]) for i in range(40)]
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked
    
    def get_color_group_probabilities(self, probabilities):
        """
        Calculate total probability for each color group.
        
        Args:
            probabilities: Array of probabilities for each space
        
        Returns:
            dict: Color group name -> total probability
        """
        from board import COLOR_GROUPS
        
        group_probabilities = {}
        for group_name, spaces in COLOR_GROUPS.items():
            total_prob = sum(probabilities[space] for space in spaces)
            group_probabilities[group_name] = total_prob
        
        return group_probabilities


def run_both_strategies(num_iterations=1_000_000, turns_per_iteration=10_000):
    """
    Run simulations for both jail strategies.
    
    Args:
        num_iterations: Number of simulations per strategy
        turns_per_iteration: Number of turns per simulation
    
    Returns:
        tuple: (probabilities_A, probabilities_B) - probability arrays for each strategy
    """
    sim = MonopolySimulation(num_iterations, turns_per_iteration)
    
    # Run Strategy A
    counts_A = sim.run_simulation(jail_strategy='A')
    probs_A = sim.calculate_probabilities(counts_A)
    
    # Run Strategy B
    counts_B = sim.run_simulation(jail_strategy='B')
    probs_B = sim.calculate_probabilities(counts_B)
    
    return probs_A, probs_B
