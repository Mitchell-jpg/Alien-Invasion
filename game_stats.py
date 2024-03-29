import pygame
from pathlib import Path
import json

class GameStats:
    """Tracks stats for the game"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # High scores should not be reset
        self.high_score = 0
        

    def reset_stats(self):
        """initialize stats that can change during gameplay"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1