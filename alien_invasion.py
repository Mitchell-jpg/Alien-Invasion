import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initilize the game, and create game resources"""
        pygame.init()

        # Set tick speed and initialize settings
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        # Set window size
        self.screen = pygame.display.set_mode(
            (1200,800))
        
        # Set caption
        pygame.display.set_caption("Alien Invasion")

        # Set background color
        self.bg_color = (230, 230, 230)

        # Create an instance to store game stats and score
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create ship instance
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create fleet instance
        self._create_fleet()

        # Start game in inactive state
        self.game_active = False

        # Draw scoreboard info
        self.sb.show_score()

        # Make play button
        self.play_button = Button(self, "Click or press 'P' to Play")


    def run_game(self):
        """Start the main loop for the game"""
        while True:
           # Keep screen and player events updated
           self._check_events()
           self._update_screen()
           self.clock.tick(60)

           # Stop gameplay if game_active flag is false
           if self.game_active:  
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

    def _start_game(self):
        """Start gamesplay"""

        #reset game statistics
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level() 
        self.sb.prep_ships() 
        self.game_active = True

        # Remove all bullets and aliens
        self.bullets.empty()
        self.aliens.empty()

        # Create new fleet and center ship
        self._create_fleet()
        self.ship.center_ship()
            
        # Hide mouse cursor during gameplay.
        pygame.mouse.set_visible(False)

        # Reset game settings
        self.settings.initialize_dynamic_settings()
                

            
    def _check_events(self):
        """Respond to keypresses and mouse movements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: 
                self._check_keydown_events(event)     
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player preses play"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        # Restarts game only if game is not active
        if button_clicked and not self.game_active:
            self._start_game()

            
        
    
    def _check_keydown_events(self, event):
        """Responds to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responds to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create bullet and add it to the bullet's group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 

    def _check_bullet_alien_collisions(self):
        """responds to bullet-alien collisions""" 
        #checks if bullet hits alien then removes bullet.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:

            #destorys existing bullets and creates new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
        
            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_bullets(self):
        """Update the position of bullets and get rid of oldbullets"""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have dissapeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        # Check for collisions
        self._check_bullet_alien_collisions()

    
    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make an alien and keep adding aliens until there is no room left
        # spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # finished a row; reset x value, increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """respond to alien reaching edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    
    def _create_alien(self, x_position, y_position):
        """create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """update the position of all aliens in fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # look for ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        """Respond to ship being hit by alien"""

        # If the player loses all their ships, end the game.

        if self.stats.ships_left > 0:
            # removes a ship from available ships, update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #removes all bullets and aliens from the screen
            self.bullets.empty()
            self.aliens.empty()

            # Initialize new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # pause game briefly
            sleep(0.5)
        else:
            self.game_active = False

            # Make mouse visible when game is not active
            pygame.mouse.set_visible(True)
    
    
    def _update_screen(self):
        """Updates images on screen, and flips to new screen"""
        # Redraw the screen during each pass of the loop
        self.screen.fill(self.settings.bg_color)
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()
        
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw scoreboard information
        self.sb.show_score()
            
        # Display play button if game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Make screen visible
        pygame.display.flip()

        

    


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()