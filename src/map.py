from dataclasses import dataclass

import pygame
import pyscroll
import pytmx
import modifyTiles as maplib


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    obstacles: list[pygame.Rect]
    chests: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap


class MapManager:

    def __init__(self, screen, player):
        self.maps = {}
        self.screen = screen
        self.player = player
        self.current_map = "niveau1"

        self.register_map(self.current_map)

        self.teleport_player("player")

        self.is_replaced = [False, False, False]
        self.chest_tiles = (819, 825, 820, 826)
        self.chest_list = (((17, 1), (17, 2), (18, 1), (18, 2)),
                           ((1, 8), (2, 8), (1, 9), (2, 9)),
                           ((1, 17), (2, 17), (1, 18), (2, 18)))

    def replace_chest(self, chest: int):
        if not self.is_replaced[chest]:
            map_class = maplib.Maptmx(f'../map/{self.current_map}.tmx')
            chests_layer = map_class.layer(8)
            for i in range(4):
                chests_layer.setTile(self.chest_tiles[i], self.chest_list[chest][i])
            map_class.autosave()
            self.is_replaced[chest] = True
            self.register_map(self.current_map)

    def check_collisions(self):
        for sprite in self.get_group().sprites():

            '''if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1'''

            if sprite.feet.collidelist(self.get_walls()) > -1 or sprite.feet.collidelist(self.get_obstacles()) !=-1:
                sprite.move_back()
            a = sprite.feet.collidelist(self.get_chest())
            if a > -1:
                self.replace_chest(a)

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name):
        # charger la carte (.tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f'../map/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())  # charger calques de map
        map_layer.zoom = 2.5

        # définir une liste qui va stocker les rectangles de collision
        walls = []
        obstacles = [pygame.Rect(0, 0, 0, 0)] * 3
        chests = [pygame.Rect(0, 0, 0, 0)] * 3

        for obj in tmx_data.objects:
            if obj.type == 'collision' or obj.type == 'wall':
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'chest':
                chests[int(obj.name)] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if obj.type == 'obstacle':
                obstacles[int(obj.name)] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        # dessiner groupe de calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        # Enregistrer la nouvelle carte chargée
        self.maps[name] = Map(name, walls, obstacles, chests, group, tmx_data)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_chest(self):
        return self.get_map().chests

    def get_obstacles(self):
        return self.get_map().obstacles

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()
