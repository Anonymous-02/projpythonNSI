import json
from typing import List, Dict, Any
import xmltodict


def rlen(x):
    return range(len(x))


class Maptmx(object):

    def __init__(self, file=None):
        super(Maptmx, self).__init__()
        self.path = ""
        self.layers = []
        self.tilesets = {}
        self.objectgroup = {}
        self.version = ""
        self.tiledversion = ""
        self.orientation = ""
        self.renderorder = ""
        self.width = ""
        self.height = ""
        self.tilewidth = ""
        self.tileheight = ""
        self.infinite = ""
        self.nextlayerid = ""
        self.nextobjectid = ""
        if file is not None:
            self.load(file)

    def save(self, path):
        file = open(path, "w")
        file.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<map version="{self.version}"'
                   f' tiledversion="{self.tiledversion}" orientation="{self.orientation}"'
                   f' renderorder="{self.renderorder}" width="{self.width}" height="{self.height}"'
                   f' tilewidth="{self.tilewidth}" tileheight="{self.tileheight}" infinite="{self.infinite}"'
                   f' nextlayerid="{self.nextlayerid}" nextobjectid="{self.nextobjectid}">')
        for i in self.tilesets:
            file.write(f'\n\t<tileset firstgid="{i["firstgid"]}" source="{i["source"]}"/>')
        for i in self.layers:
            file.write(f'\n\t<layer id="{i.id}" name="{i.name}" width="{i.size["width"]}" height="{i.size["height"]}">')
            file.write(f'\n\t\t<data encoding="{i.encoding}">')
            txt = ""
            for j in i.grid:
                txt += "\n"
                for k in j:
                    txt += str(k) + ","
            file.write(txt[:-1])
            file.write("\n\t\t</data>\n\t</layer>")
        a = self.objectgroup
        file.write(f'\n\t<objectgroup id="{a["id"]}" name="{a["name"]}">')
        for i in a["object"]:
            if i["type"] == 'obstacle' or i['type'] == "pnj" or i['type'] == "chest":
                file.write(f'\n\t\t<object id="{i["id"]}" name="{i["name"]}" type="{i["type"]}" x="{i["x"]}" y="{i["y"]}"'
                           f' width="{i["width"]}" height="{i["height"]}"/>')
            elif i["type"] == 'player':
                file.write(f'\n\t\t<object id="{i["id"]}" name="{i["name"]}" type="{i["type"]}" x="{i["x"]}"'
                           f' y="{i["y"]}">\n\t\t\t<point/>\n\t\t</object>')
            else:
                file.write(f'\n\t\t<object id="{i["id"]}" type="{i["type"]}" x="{i["x"]}" y="{i["y"]}"'
                           f' width="{i["width"]}" height="{i["height"]}"/>')
        file.write("\n\t</objectgroup>\n</map>")
        file.close()

    def autosave(self):
        self.save(self.path)

    def layer(self, pos):
        if type(pos) == int:
            for i in self.layers:
                if pos == i.id:
                    # print(f"layer {i.name} at pos {i.id} of size {i.size['height']}x{i.size['width']}")
                    return i
        elif type(pos) == str:
            for i in self.layers:
                if pos == i.name:
                    # print(f"layer {i.name} at pos {i.id} of size {i.size['height']}x{i.size['width']}")
                    return i
        print("this layer doesn't exist")

    def load_values(self, dic):
        for i in dic['layer']:
            self.layers.append(MapLayer(i["id"], i['name'], i['height'], i['width'],
                                        i['data']['text'], i['data']['encoding']))
        self.height = dic["@height"]
        self.infinite = dic["@infinite"]
        self.nextlayerid = dic["@nextlayerid"]
        self.nextobjectid = dic["@nextobjectid"]
        self.objectgroup = dic["objectgroup"]
        self.orientation = dic["@orientation"]
        self.renderorder = dic['@renderorder']
        self.tiledversion = dic['@tiledversion']
        self.tileheight = dic['@tileheight']
        self.tilesets = dic['tileset']
        self.tilewidth = dic['@tilewidth']
        self.version = dic['@version']
        self.width = dic['@width']

    def load(self, path: str) -> None:
        self.path = path
        file = open(path, "r")
        dico = xmltodict.parse(file.read())["map"]
        lay = dico["layer"]
        lay2 = []
        for i in range(len(lay)):
            lay2 += [{}]
            for j in lay[i]:
                if j[0] == "@":
                    lay2[i][j[1:]] = lay[i][j]
                elif j == "data":
                    lay2[i]["data"] = {}
                    for k in lay[i]["data"]:
                        lay2[i]["data"][k[1:]] = lay[i]["data"][k]
                else:
                    lay2[i][j] = lay[i][j]
        obj = dico["objectgroup"]
        obj2 = {}
        for i in obj:
            if i[0] == "@":
                obj2[i[1:]] = obj[i]
            else:
                obj2['object'] = []
                for j in rlen(obj["object"]):
                    obj2['object'] += [{}]
                    for k in obj[i][j]:
                        obj2[i][j][k[1:]] = obj[i][j][k]
        tls = dico["tileset"]
        tls2 = []
        for i in rlen(tls):
            tls2.append({})
            for j in tls[i]:
                tls2[i][j[1:]] = tls[i][j]
        dico["layer"] = lay2
        dico["objectgroup"] = obj2
        dico["tileset"] = tls2
        file = open("test.json", "w")
        file.write(json.dumps(dico, sort_keys=True, indent=2))
        file.close()
        self.load_values(dico)


class MapLayer(object):
    def __init__(self, i_d, name, height, width, data, encoding):
        self.id = int(i_d)
        self.name = name
        self.size = {'height': int(height), 'width': int(width)}
        grid = []
        for i in data.split('\n'):
            grid.append(i.split(','))
        for i in range(len(grid)-1):
            grid[i].pop()
        self.grid = grid
        self.encoding = encoding

    def getTile(self, x, y=0):
        if type(x) == list:
            y = x[1]
            x = x[0]
        return self.grid[x][y]

    def setTile(self, value=None, coord=(0, 0)):
        if value is None:
            value = self.grid[coord[1]][coord[0]]
        print(f"the tile at {coord[0]}:{coord[1]} got set to {value}")
        self.grid[coord[1]][coord[0]] = value
