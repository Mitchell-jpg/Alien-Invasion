class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """initialize games static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        #bullet settings
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        #alien settings
        self.fleet_drop_speed = 30

        # Score settings
        self.alien_points = 50

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly points value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    
    def initialize_dynamic_settings(self):
        """Initilize settings throught the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # Fleet_direction of 1 represents right; -1 left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        