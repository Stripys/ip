import random
import math
import pygame
import numpy as np
from scipy.ndimage import gaussian_filter
import pygame.surfarray as surfarray
import os

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
TILE_SIZE = 64
X = 30
Y = 17

RECORDS_FILE = "records.txt"
current_level = 1
max_level = 0

def load_record():
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, 'r') as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_record(level):
    with open(RECORDS_FILE, 'w') as f:
        f.write(str(level))

max_level = load_record()

class Arrow:
    def __init__(self, x, y, angle, speed):
        self.position = [x, y]
        self.angle = angle
        self.speed = speed
        self.original_image = pygame.image.load('arrow.png').convert_alpha()
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angle))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, map):
        self.position[0] += math.cos(self.angle) * self.speed
        self.position[1] += math.sin(self.angle) * self.speed
        self.rect.center = self.position

        tile_x = int(self.position[0] // TILE_SIZE)
        tile_y = int(self.position[1] // TILE_SIZE)
        if 0 <= tile_y < len(map) and 0 <= tile_x < len(map[0]):
            if map[tile_y][tile_x].content == r'2.png':
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        return (self.position[0] < 0 or self.position[0] > screen_width or
                self.position[1] < 0 or self.position[1] > screen_height)


class Player:
    def __init__(self, texture, spawn):
        self.texture = texture
        self.position = [spawn[0] * TILE_SIZE, spawn[1] * TILE_SIZE]
        self.speed = [5, 5]
        self.original_image = pygame.image.load(self.texture).convert_alpha()
        self.image = self.original_image
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = self.position
        self.prev_position = self.position.copy()
        self.arrows = []
        self.health = 100
        self.last_damage_time = pygame.time.get_ticks()
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 100
        self.fov = 60
        self.view_distance = 300
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.position[0], mouse_y - self.position[1]
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=old_center)

    def move(self, map):
        self.prev_position = self.position.copy()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position[1] -= self.speed[1]
        if keys[pygame.K_s]:
            self.position[1] += self.speed[1]
        if keys[pygame.K_a]:
            self.position[0] -= self.speed[0]
        if keys[pygame.K_d]:
            self.position[0] += self.speed[0]
        self.rect.center = self.position

        tile_x = int(self.position[0] // 64)
        tile_y = int(self.position[1] // 64)

        if map[tile_y][tile_x].content == r'2.png':
            self.position = self.prev_position
            self.rect.center = self.position

            temp_position = self.position.copy()
            temp_position[0] += self.speed[0] if keys[pygame.K_d] else -self.speed[0] if keys[pygame.K_a] else 0
            tile_x_new = int(temp_position[0] // 64)
            tile_y_new = int(temp_position[1] // 64)

            if map[tile_y_new][tile_x_new].content != r'2.png':
                self.position = temp_position

            temp_position = self.position.copy()
            temp_position[1] += self.speed[1] if keys[pygame.K_s] else -self.speed[1] if keys[pygame.K_w] else 0
            tile_x_new = int(temp_position[0] // 64)
            tile_y_new = int(temp_position[1] // 64)

            if map[tile_y_new][tile_x_new].content != r'2.png':
                self.position = temp_position

            self.rect.center = self.position

        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.position[0] = max(16, min(screen_width - 16, self.position[0]))
        self.position[1] = max(16, min(screen_height - 16, self.position[1]))
        self.rect.center = self.position

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.position[0], mouse_y - self.position[1]
            angle = math.atan2(rel_y, rel_x)
            speed = 10
            arrow = Arrow(self.position[0], self.position[1], angle, speed)
            self.arrows.append(arrow)
            self.last_shot_time = current_time

    def update_arrows(self, map, enemies):
        for arrow in self.arrows[:]:
            if arrow.update(map) or arrow.is_off_screen():
                self.arrows.remove(arrow)
            else:
                for enemy in enemies[:]:
                    if arrow.rect.colliderect(enemy.rect):
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                        self.arrows.remove(arrow)
                        break

    def draw_arrows(self, screen):
        for arrow in self.arrows:
            arrow.draw(screen)

    def regenerate_health(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_damage_time > 3000:
            self.health = min(100, self.health + 1)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        self.last_damage_time = pygame.time.get_ticks()

    def draw_health(self, screen):
        pass
        pygame.draw.rect(screen, (255, 0, 0), (self.position[0] - 50, self.position[1] - 70, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0] - 50, self.position[1] - 70, self.health, 10))

class Enemy:
    def __init__(self, x, y):
        self.position = [x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2]
        self.speed = 3
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2))
        self.vision_radius = 256
        self.health = 1
        self.last_attack_time = pygame.time.get_ticks()

    def move_towards_player(self, player_position, map):
        dx = player_position[0] - self.position[0]
        dy = player_position[1] - self.position[1]
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance

        new_position = [self.position[0] + dx * self.speed, self.position[1] + dy * self.speed]
        tile_x = int(new_position[0] // TILE_SIZE)
        tile_y = int(new_position[1] // TILE_SIZE)

        if 0 <= tile_y < len(map) and 0 <= tile_x < len(map[0]):
            if map[tile_y][tile_x].content != r'2.png':
                self.position = new_position
                self.rect.center = self.position

    def can_see_player(self, player_position, map):
        dx = player_position[0] - self.position[0]
        dy = player_position[1] - self.position[1]
        distance = math.hypot(dx, dy)
        if distance > self.vision_radius:
            return False

        steps = int(distance)
        for i in range(steps):
            x = int(self.position[0] + dx * i / steps)
            y = int(self.position[1] + dy * i / steps)
            tile_x = x // TILE_SIZE
            tile_y = y // TILE_SIZE
            if 0 <= tile_y < len(map) and 0 <= tile_x < len(map[0]):
                if map[tile_y][tile_x].content == r'2.png':
                    return False
        return True

    def attack_player(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > 1000:
            player.take_damage(10)
            self.last_attack_time = current_time

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Tile():
    def __init__(self, tile_type: int):
        self.typee = tile_type
        self.content = f'{tile_type}.png'
        self.image = pygame.image.load(self.content).convert_alpha()



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
            b = a

            for i in range(y):
                self.map[i][b] = Tile(3)
        for i in range(4):
            a = random.randint(mini, y-mini)
            n=0
            map = self.map
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

        for i in range(5):
            self.spawn_x = random.randint(1, x - 2)
            self.spawn_y = random.randint(1, y - 2)
            while self.map[self.spawn_y][self.spawn_x].typee != 0:
                self.spawn_x = random.randint(1, x-2)
                self.spawn_y = random.randint(1, y-2)
            self.map[self.spawn_y][self.spawn_x] = Tile(4)
            self._build_house(self.spawn_x, self.spawn_y)

        self.spawn_x = random.randint(1, x - 2)
        self.spawn_y = random.randint(1, y - 2)
        while self.map[self.spawn_y][self.spawn_x].typee != 1:
            self.spawn_x = random.randint(1, x - 2)
            self.spawn_y = random.randint(1, y - 2)

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j].typee == 3 or self.map[i][j].typee == 4:
                    self.map[i][j] = Tile(0)
        self.map[0][0] = Tile(2)
        print(self)


    def _build_house(self, X = 30, Y = 17, rand = False):

        if rand:
            X = random.randint(1, self.x - 2)
            Y = random.randint(1, self.y - 2)

            while self.map[self.spawn_y][self.spawn_x].typee != 0:
                X = random.randint(1, x - 2)
                Y = random.randint(1, y - 2)

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
            y0 = 0
            pass

        try:
            y1 = self.spawn_y + down_spawn.index(3)
        except ValueError:
            y1 = self.y - 1
            pass

        try:
            x0 = self.spawn_x - left_spawn.index(3)
        except ValueError:
            x0 = 0
            pass

        try:
            x1 = self.spawn_x + right_spawn.index(3)
        except ValueError:
            x1 = self.x - 1
            pass

        house_coords = [[x0, y0],[x1, y1]]
        for i in range(y1 - y0 + 1):
            for j in range(x1 - x0 + 1):
                try:
                    if self.map[i+y0][j+x0].typee == 3:
                        self.map[i+y0][j+x0] = Tile(2)
                    elif self.map[i+y0][j+x0].typee == 0:
                        self.map[i+y0][j+x0] = Tile(1)
                except IndexError:
                    pass

        self.map[self.spawn_y][self.spawn_x] = Tile(1)
        self.map[y0][random.randint(x0 + 1, x1 - 1)] = Tile(1)
        self.map[y1][random.randint(x0 + 1, x1 - 1)] = Tile(1)
        self.map[random.randint(y0 + 1, y1 - 1)][x0] = Tile(1)
        self.map[random.randint(y0 + 1, y1 - 1)][x1] = Tile(1)

    def __str__(self):
        strr = ''
        for i in range(self.y):
            for j in range(self.x):
                strr += str(self.map[i][j].typee)
                strr += ' '
            strr += '\n'
        return strr

def spawn_enemies(map, count, player_pos, enmy_dov = 5):
    enemies = []
    print(spawn)
    occupied_tiles = set()
    for _ in range(count):
        while True:
            x = random.randint(0, len(map.map[0]) - 1)
            y = random.randint(0, len(map.map) - 1)

            dx = abs(player_pos[0] - x)
            dy = abs(player_pos[1] - y)
            distance = math.hypot(dx, dy)
            print(distance)
            if (map.map[y][x].typee == 0 or map.map[y][x].typee == 1) and (x, y) not in occupied_tiles and distance>=enmy_dov:
                enemies.append(Enemy(x, y))
                occupied_tiles.add((x, y))
                break
    return enemies


class Button:
    def __init__(self, x, y, text, font_size=30, typ = False):
        self.image = pygame.image.load('Button.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (244, 124))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.font = pygame.font.Font('overdozesans.ttf', font_size)
        self.text_surf = self.font.render(text, True, BLACK)

        if typ:
            self.image = pygame.image.load('pause.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        screen.blit(self.text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def apply_gaussian_blur(surface, sigma=5):
    array = surfarray.array3d(surface)
    blurred_array = gaussian_filter(array, sigma=(sigma, sigma, 0))
    return surfarray.make_surface(blurred_array)


display = pygame.display.set_mode(flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()
karta = Map(X, Y)
karta.generate(30, 17)
spawn = karta.spawn_x, karta.spawn_y
play = Player('player_test.png', spawn)
enemies = spawn_enemies(karta, 50, spawn, 5)
MAP = karta.map
screen_width, screen_height = pygame.display.get_surface().get_size()

button_start = Button(screen_width // 2 - 122, screen_height // 2 - 150, "Новая игра")
button_load = Button(screen_width // 2 - 122, screen_height // 2, "Продолжить игру")
button_exit = Button(screen_width // 2 - 122, screen_height // 2 + 150, "Выйти")

button_death_exit = Button(screen_width // 2 - 122, screen_height // 2 + 50, "Выйти из игры")
button_death_menu = Button(screen_width // 2 - 122, screen_height // 2 - 100, "Обратно в меню")

button_resume = Button(screen_width // 2 - 122, screen_height // 2 - 200, "Продолжить игру")
button_pause_menu = Button(screen_width // 2 - 122, screen_height // 2 - 50, "Выйти в меню")
button_restart = Button(screen_width // 2 - 122, screen_height // 2 + 100, "Рестарт")
button_pause_exit = Button(screen_width // 2 - 122, screen_height // 2 + 250, "Выйти из игры")

button_pause = Button(0, 0, '', typ=True)

button_win_next = Button(screen_width // 2 - 122, screen_height // 2 - 50, "Следующий уровень")
button_win_menu = Button(screen_width // 2 - 122, screen_height // 2 + 100, "В меню")

show_pause_menu = False
show_menu = True
is_dead = False
is_win = False
font = pygame.font.Font('overdozesans.ttf', 74)
small_font = pygame.font.Font('overdozesans.ttf', 36)

run = True
while run:
    if show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and show_menu:
                if button_start.is_clicked(event.pos):
                    show_menu = False
                    current_level = 1
                    karta.generate(30, 17)
                    spawn = karta.spawn_x, karta.spawn_y
                    play = Player('player_test.png', spawn)
                    enemies = spawn_enemies(karta, 50, spawn, 5)
                elif button_load.is_clicked(event.pos):
                    show_menu = False
                elif button_exit.is_clicked(event.pos):
                    run = False

        display.fill(WHITE)
        text = font.render("Random combat", True, BLACK)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 300))
        display.blit(text, text_rect)

        record_text = small_font.render(f"Рекорд: {max_level}", True, BLACK)
        record_rect = record_text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))
        display.blit(record_text, record_rect)

        button_start.draw(display)
        button_load.draw(display)
        button_exit.draw(display)

    elif is_dead:
        blurred_background = apply_gaussian_blur(background_surface, sigma=3)
        display.blit(blurred_background, (0, 0))
        death_text = font.render("Вы проиграли", True, RED)
        death_text_rect = death_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        display.blit(death_text, death_text_rect)

        level_text = small_font.render(f"Достигнут уровень: {current_level}", True, BLACK)
        level_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2 - 115))
        display.blit(level_text, level_rect)

        button_death_exit.draw(display)
        button_death_menu.draw(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_death_exit.is_clicked(event.pos):
                    run = False
                elif button_death_menu.is_clicked(event.pos):
                    is_dead = False
                    show_menu = True
                    current_level = 1
                    play = Player('player_test.png', spawn)
                    enemies = spawn_enemies(karta, 50, spawn, 5)

    elif is_win:
        blurred_background = apply_gaussian_blur(background_surface, sigma=3)
        display.blit(blurred_background, (0, 0))
        win_text = font.render("Победа!", True, GREEN)
        win_text_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        display.blit(win_text, win_text_rect)

        level_text = small_font.render(f"Уровень {current_level} пройден!", True, BLACK)
        level_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2 - 70))
        display.blit(level_text, level_rect)

        button_win_next.draw(display)
        button_win_menu.draw(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_win_next.is_clicked(event.pos):
                    is_win = False
                    current_level += 1
                    if current_level > max_level:
                        max_level = current_level
                        save_record(max_level)
                    karta.generate(30, 17)
                    spawn = karta.spawn_x, karta.spawn_y
                    play = Player('player_test.png', spawn)
                    enemies = spawn_enemies(karta, 50 + current_level * 5, spawn, 5)
                elif button_win_menu.is_clicked(event.pos):
                    is_win = False
                    show_menu = True

    elif show_pause_menu:
        blurred_background = apply_gaussian_blur(background_surface, sigma=3)
        display.blit(blurred_background, (0, 0))
        pause_text = font.render("Пауза", True, BLACK)
        pause_text_rect = pause_text.get_rect(center=(screen_width // 2, screen_height // 2 - 300))
        display.blit(pause_text, pause_text_rect)

        level_text = small_font.render(f"Уровень: {current_level}", True, WHITE)
        level_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))
        display.blit(level_text, level_rect)

        button_resume.draw(display)
        button_pause_menu.draw(display)
        button_restart.draw(display)
        button_pause_exit.draw(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_resume.is_clicked(event.pos):
                    show_pause_menu = False
                elif button_pause_menu.is_clicked(event.pos):
                    show_pause_menu = False
                    show_menu = True
                elif button_restart.is_clicked(event.pos):
                    show_pause_menu = False
                    karta.generate(30, 17)
                    spawn = karta.spawn_x, karta.spawn_y
                    play = Player('player_test.png', spawn)
                    enemies = spawn_enemies(karta, 50, spawn, 5)
                elif button_pause_exit.is_clicked(event.pos):
                    run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_pause_menu = False

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_pause.is_clicked(event.pos):
                    show_pause_menu = True
                    background_surface = display.copy()
                else:
                    play.shoot()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_pause_menu = True
                    background_surface = display.copy()

        display.fill((220, 220, 220))

        for i in range(len(karta.map)):
            for j in range(len(karta.map[0])):
                display.blit(karta.map[i][j].image, (j * TILE_SIZE, i * TILE_SIZE))

        play.rotate()
        play.move(karta.map)
        play.update_arrows(karta.map, enemies)
        play.draw_arrows(display)
        play.regenerate_health()
        play.draw_health(display)
        display.blit(play.image, play.rect)

        for enemy in enemies[:]:
            if enemy.can_see_player(play.position, karta.map):
                enemy.move_towards_player(play.position, karta.map)
                if math.hypot(play.position[0] - enemy.position[0], play.position[1] - enemy.position[1]) < 50:
                    enemy.attack_player(play)
            enemy.draw(display)

        if play.health <= 0:
            is_dead = True
            play.draw_health(display)
            background_surface = display.copy()

        if len(enemies) == 0:
            is_win = True
            background_surface = display.copy()

        level_text = small_font.render(f"Уровень: {current_level}", True, BLACK)
        display.blit(level_text, (80, 20))

        button_pause.draw(display)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

