import pygame


class Ball:
    def __init__(self, x, y, radius=25, step=20, screen_width=800, screen_height=600):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (255, 0, 0)

    def move_up(self):
        if self.y - self.radius - self.step >= 0:
            self.y -= self.step

    def move_down(self):
        if self.y + self.radius + self.step <= self.screen_height:
            self.y += self.step

    def move_left(self):
        if self.x - self.radius - self.step >= 0:
            self.x -= self.step

    def move_right(self):
        if self.x + self.radius + self.step <= self.screen_width:
            self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)