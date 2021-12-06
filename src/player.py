import pygame

from src.animation import AnimateSprite


class Entity(AnimateSprite):  # Sprite : élément graphique du jeu qui peut intéragir avec d'autre Sprite /
    # Quelque chose de non statique
    def __init__(self, name, x, y):
        super().__init__(name)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])  # enlever le fond noir du joueur
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()

    def move_right(self): self.position[0] += self.speed

    def move_left(self): self.position[0] -= self.speed

    def move_up(self): self.position[1] -= self.speed

    def move_down(self): self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):

    def __init__(self):
        super().__init__("player", 0, 0)