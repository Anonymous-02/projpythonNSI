import pygame
import pytmx
import pyscroll

from player import Player


class Game:

    def __init__(self):
        # créer fenêtre du jeu
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption('Escape Game')

        # charger la carte (.tmx)
        tmx_data = pytmx.util_pygame.load_pygame('../map/niveau1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())  # charger calques de map
        map_layer.zoom = 2.5

        # générer un joueur
        player_position = tmx_data.get_object_by_name('player')
        self.player = Player(player_position.x, player_position.y)

        # définir une liste qui va stocker les rectangles de collision
        self.walls = []

        # recuperer les events tiled
        chest_hache = tmx_data.get_object_by_name('chest_hache')
        self.chest_hache_rect = pygame.Rect(chest_hache.x, chest_hache.y, chest_hache.width, chest_hache.height)

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        self.group.add(self.player)

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
        self.group.update()
        # event tiled
        if self.player.feet.colliderect(self.chest_hache_rect):
            pass
        # vérification collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        # boucle maintient fenêtre ouverte
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()  # actualiser à chaque tour de boucle

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)  # FPS

        pygame.quit()
