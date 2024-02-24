import pygame.font

class Button:
    """A button class to build buttons for the game"""

    def __init__(self, ai_game, msg):
        """initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set demintions and properties of the button
        self.width, self.height = 500, 200
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build buttons rect and center it.
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into rendered image and center text on screen"""
        # Call to font.render and store the output in msg_image with antialising ON
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)

        # Store the font that has been rendered to an image into a rect and center it
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draws blank button and then draw the message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)