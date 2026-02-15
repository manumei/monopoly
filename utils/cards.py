"""
Chance and Community Chest Card Decks
Handles card drawing and movement logic for special cards.
"""

import random
from board import RAILROAD_SPACES, UTILITY_SPACES, GO_SPACE, JAIL_SPACE


class Card:
    """Base class for Chance and Community Chest cards."""
    
    def __init__(self, name, affects_position=False):
        self.name = name
        self.affects_position = affects_position
    
    def apply(self, current_position):
        """
        Apply card effect.
        Returns: (new_position, in_jail_status)
        """
        return current_position, False


class AdvanceToCard(Card):
    """Card that advances player to a specific space."""
    
    def __init__(self, name, target_space):
        super().__init__(name, affects_position=True)
        self.target_space = target_space
    
    def apply(self, current_position):
        return self.target_space, False


class GoToJailCard(Card):
    """Card that sends player to jail."""
    
    def __init__(self):
        super().__init__("Go to Jail", affects_position=True)
    
    def apply(self, current_position):
        return JAIL_SPACE, True


class GoBackCard(Card):
    """Card that moves player back 3 spaces."""
    
    def __init__(self):
        super().__init__("Go Back 3 Spaces", affects_position=True)
    
    def apply(self, current_position):
        new_position = (current_position - 3) % 40
        return new_position, False


class NearestRailroadCard(Card):
    """Card that advances to nearest railroad."""
    
    def __init__(self):
        super().__init__("Advance to Nearest Railroad", affects_position=True)
    
    def apply(self, current_position):
        # Find the next railroad clockwise
        for railroad in RAILROAD_SPACES:
            if railroad > current_position:
                return railroad, False
        # If no railroad ahead, wrap to first railroad
        return RAILROAD_SPACES[0], False


class NearestUtilityCard(Card):
    """Card that advances to nearest utility."""
    
    def __init__(self):
        super().__init__("Advance to Nearest Utility", affects_position=True)
    
    def apply(self, current_position):
        # Find the next utility clockwise
        for utility in UTILITY_SPACES:
            if utility > current_position:
                return utility, False
        # If no utility ahead, wrap to first utility
        return UTILITY_SPACES[0], False


class Deck:
    """Base class for card decks with shuffling and drawing."""
    
    def __init__(self, cards):
        self.all_cards = cards
        self.cards = []
        self.shuffle()
    
    def shuffle(self):
        """Shuffle all cards back into the deck."""
        self.cards = self.all_cards.copy()
        random.shuffle(self.cards)
    
    def draw(self):
        """Draw a card from the deck. Reshuffle if empty."""
        if not self.cards:
            self.shuffle()
        return self.cards.pop()


class ChanceDeck(Deck):
    """Chance card deck with 16 cards."""
    
    def __init__(self):
        cards = [
            AdvanceToCard("Advance to GO", GO_SPACE),
            AdvanceToCard("Advance to Illinois Avenue", 24),
            AdvanceToCard("Advance to St. Charles Place", 11),
            NearestRailroadCard(),
            NearestRailroadCard(),
            NearestUtilityCard(),
            GoBackCard(),
            AdvanceToCard("Advance to Boardwalk", 39),
            GoToJailCard(),
        ]
        
        for i in range(7):
            cards.append(Card(f"No Movement {i}", affects_position=False))
        
        super().__init__(cards)

class CommunityChestDeck(Deck):
    """Community Chest card deck with 16 cards."""
    
    def __init__(self):
        cards = [
            AdvanceToCard("Advance to GO", GO_SPACE),
            GoToJailCard(),
        ]
        # Add 14 cards that don't affect position
        for i in range(14):
            cards.append(Card(f"No Movement {i}", affects_position=False))
        
        super().__init__(cards)

def create_decks():
    """Create and return new Chance and Community Chest decks."""
    return ChanceDeck(), CommunityChestDeck()
