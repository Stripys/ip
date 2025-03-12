import random
import os
import pygame

MAP = [
    [2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 0, 0, 2, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
    [2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 1, 1, 1, 2],
    [2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 2],
    [2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1, 1, 1, 2],
    [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2],
    ]


class Tile():
    def __init__(self, tile_type: int):
        self.typee = tile_type
        self.content = f'{tile_type}.png'
        #self.image = pygame.image.load(self.content).convert_alpha()



class Map():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.map = self.blank(x, y)

    def import_map(self, mapa):
        self.map = [[Tile(mapa[i][j]) for j in range(x)] for i in range(y)]

    def blank(self, x, y):
        mapa = list()
        for i in range(y):
            row = list()
            for j in range(x):
                tile = Tile(0)
                row.append(tile)
            mapa.append(row)
        return mapa

    def generate(self, x = 30, y = 17):
        self.x = x
        self.y = y
        self.map = self.blank(x, y)
        mini = 4
        tryy = 100
        a = 0
        b = 0
        for i in range(4):
            a = random.randint(mini, x-mini)
            while self.map[0][a-3].typee!=0 or self.map[0][a-2].typee!=0 or self.map[0][a-1].typee!=0 or self.map[0][a].typee!=0 or self.map[0][a+1].typee!=0 or self.map[0][a+2].typee!=0 or self.map[0][a+3].typee!=0:
                a = random.randint(mini, x-mini)
                print(a)
            b = a

            for i in range(y):
                self.map[i][b] = Tile(3)
        for i in range(4):
            a = random.randint(mini, y-mini)
            n=0
            map = self.map
            print(self)
            b = True
            while not (self.map[a-2][0].typee==0 and self.map[a-1][0].typee==0 and self.map[a][0].typee==0 and self.map[a+1][0].typee==0 and self.map[a+2][0].typee==0):
                n+=1
                a = random.randint(mini, y-mini)
                if n>= tryy:
                    b = False
                    break
            if b:
                c = a
                for i in range(x):
                    self.map[c][i] = Tile(3)

        self.spawn_x = random.randint(1, x-2)
        self.spawn_y = random.randint(1, y-2)

        while self.map[self.spawn_y][self.spawn_x].typee != 0:
            self.spawn_x = random.randint(1, x-2)
            self.spawn_y = random.randint(1, y-2)

        self.map[self.spawn_y][self.spawn_x].typee = 4

        X = self.spawn_x
        Y = self.spawn_y

        self._build_house(self.spawn_x, self.spawn_y)


    def _build_house(self, X, Y, rand = False):

        if rand:
            X = random.randint(1, x - 2)
            Y = random.randint(1, y - 2)

            while self.map[self.spawn_y][self.spawn_x].typee != 0:
                X = random.randint(1, x - 2)
                Y = random.randint(1, y - 2)

        mapa = self.map
        row = list()
        for i in range(self.x):
            row.append(self.map[self.spawn_y][i].typee)
        column = list()
        for i in range(self.y):
            column.append(self.map[i][self.spawn_x].typee)

        up_spawn = column[:Y+1]
        down_spawn = column[Y:]
        up_spawn.reverse()

        right_spawn = row[X:]
        left_spawn = row[:X+1]
        left_spawn.reverse()

        y0 = -1
        y1 = -1
        x0 = -1
        x1 = -1

        try:
            y0 = self.spawn_y - up_spawn.index(3)
        except ValueError:
            print('up_spawn')
            y0 = 0
            pass

        try:
            y1 = self.spawn_y + down_spawn.index(3)
        except ValueError:
            print('down_spawn')
            y1 = self.y - 1
            pass

        try:
            x0 = self.spawn_x - left_spawn.index(3)
        except ValueError:
            print('left_spawn')
            x0 = 0
            pass

        try:
            x1 = self.spawn_x + right_spawn.index(3)
        except ValueError:
            print('right_spawn')
            x1 = self.x - 1
            pass

        house_coords = [[x0, y0],[x1, y1]]
        print(house_coords)
        for i in range(y1 - y0 + 1):
            for j in range(x1 - x0 + 1):
                try:
                    if self.map[i+y0][j+x0].typee == 3:
                        self.map[i+y0][j+x0].typee = 2
                    elif self.map[i+y0][j+x0].typee == 0:
                        self.map[i+y0][j+x0].typee = 1
                except IndexError:
                    pass





    def __str__(self):
        strr = ''
        for i in range(self.y):
            for j in range(self.x):
                strr += str(self.map[i][j].typee)
                strr += ' '
            strr += '\n'
        return strr


karta = Map(30, 17)
karta.generate()
print(karta)