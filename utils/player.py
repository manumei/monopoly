"""
Player Movement Logic
Handles player state, dice rolling, movement, and jail mechanics.
"""

import random
from utils.board import (
    is_chance, is_community_chest, GO_TO_JAIL_SPACE, 
    JAIL_SPACE, GO_SPACE
)


class Player:
    """Represents a player with position, jail state, and movement logic."""
    
    def __init__(self, jail_strategy='A'):
        """
        Initialize player at GO.
        
        Args:
            jail_strategy: 'A' (stay in jail as long as possible) or 
                          'B' (leave jail immediately)
        """
        self.position = GO_SPACE
        self.in_jail = False
        self.jail_turns = 0
        self.consecutive_doubles = 0
        self.jail_strategy = jail_strategy
    
    def roll_dice(self):
        """
        Roll two six-sided dice.
        
        Returns:
            tuple: (die1, die2, total, is_doubles)
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        is_doubles = (die1 == die2)
        return die1, die2, total, is_doubles
    
    def move_forward(self, spaces):
        """Move player forward by a number of spaces."""
        self.position = (self.position + spaces) % 40
    
    def move_to(self, space):
        """Move player to a specific space."""
        self.position = space
    
    def send_to_jail(self):
        """Send player to jail."""
        self.position = JAIL_SPACE
        self.in_jail = True
        self.jail_turns = 0
        self.consecutive_doubles = 0
    
    def handle_jail_turn(self):
        """
        Handle a turn while in jail.
        
        Returns:
            int or None: Number of spaces to move if leaving jail, None otherwise
        """
        # Strategy B: Leave jail immediately (pay fine/use card)
        if self.jail_strategy == 'B':
            self.in_jail = False
            self.jail_turns = 0
            die1, die2, total, is_doubles = self.roll_dice()
            return total
        else:
            # Strategy A: Try to stay in jail (only leave if forced)
            die1, die2, total, is_doubles = self.roll_dice()
            
            if is_doubles:
                # Got doubles - must leave jail
                self.in_jail = False
                self.jail_turns = 0
                return total
            
            self.jail_turns += 1
            
            if self.jail_turns >= 3:
                # Forced out after 3 turns
                self.in_jail = False
                self.jail_turns = 0
                return total
            
            # Stay in jail
            return None
    
    def take_turn(self, chance_deck, community_chest_deck):
        """
        Execute one complete turn, including all movements and card draws.
        
        Returns:
            int: Final position after all movements are complete
        """
        # Handle jail turns separately
        if self.in_jail:
            move_amount = self.handle_jail_turn()
            if move_amount is not None:
                # Leaving jail - move from jail space
                self.move_forward(move_amount)
                # Process landing (could land on card or Go to Jail)
                return self._process_landing(chance_deck, community_chest_deck)
            else:
                # Still in jail
                return self.position
        
        # Normal turn: roll dice
        die1, die2, total, is_doubles = self.roll_dice()
        
        if is_doubles:
            self.consecutive_doubles += 1
            if self.consecutive_doubles >= 3:
                # Three doubles in a row - go to jail
                self.send_to_jail()
                return self.position
        else:
            self.consecutive_doubles = 0
        
        # Move forward
        self.move_forward(total)
        
        # Process landing and return final position
        return self._process_landing(chance_deck, community_chest_deck)
    
    def _process_landing(self, chance_deck, community_chest_deck):
        """
        Process landing on a space (handle special spaces and cards).
        
        Returns:
            int: Final position after all forced movements
        """
        # Check for Go to Jail space
        if self.position == GO_TO_JAIL_SPACE:
            self.send_to_jail()
            return self.position
        
        # Check for Chance
        if is_chance(self.position):
            card = chance_deck.draw()
            if card.affects_position:
                new_position, go_to_jail = card.apply(self.position)
                self.position = new_position
                if go_to_jail:
                    self.in_jail = True
                    self.jail_turns = 0
                    self.consecutive_doubles = 0
                    return self.position
                # Recursively process new landing (e.g., "Go Back 3" could land on Community Chest)
                return self._process_landing(chance_deck, community_chest_deck)
        
        # Check for Community Chest
        if is_community_chest(self.position):
            card = community_chest_deck.draw()
            if card.affects_position:
                new_position, go_to_jail = card.apply(self.position)
                self.position = new_position
                if go_to_jail:
                    self.in_jail = True
                    self.jail_turns = 0
                    self.consecutive_doubles = 0
                    return self.position
                # Recursively process new landing
                return self._process_landing(chance_deck, community_chest_deck)
        
        return self.position
