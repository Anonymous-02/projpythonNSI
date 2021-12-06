import pygame
import pytmx
import pyscroll

from player import Player
from src.map import MapManager


class Game:

    def __init__(self):
        # créer fenêtre du jeu
        self.screen = pygame.display.set_mode((1080, 650))
        pygame.display.set_caption('Escape Game')

        # générer un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def update(self):
        self.map_manager.update()

    def run(self):

        clock = pygame.time.Clock()

        # boucle maintient fenêtre ouverte
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            pygame.display.flip()  # actualiser à chaque tour de boucle

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)  # FPS

        pygame.quit()
