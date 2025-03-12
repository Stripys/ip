import random
import math
import pygame

# Инициализация Pygame
pygame.init()

# Константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
TILE_SIZE = 64
SPAWN = [2, 2]

# Загрузка карты
MAP = [
    [2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 0, 0, 2, 0, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0],
    [2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Класс стрелы
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

        # Проверка на столкновение со стеной
        tile_x = int(self.position[0] // TILE_SIZE)
        tile_y = int(self.position[1] // TILE_SIZE)
        if 0 <= tile_y < len(map) and 0 <= tile_x < len(map[0]):
            if map[tile_y][tile_x].content == r'2.png':
                return True  # Стрела должна быть удалена
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        return (self.position[0] < 0 or self.position[0] > screen_width or
                self.position[1] < 0 or self.position[1] > screen_height)

# Класс игрока
class Player:
    def __init__(self, texture, spawn):
        self.texture = texture
        self.position = [spawn[0] * TILE_SIZE, spawn[1] * TILE_SIZE]
        self.speed = [3, 3]
        self.original_image = pygame.image.load(self.texture).convert_alpha()
        self.image = self.original_image
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = self.position
        self.prev_position = self.position.copy()
        self.arrows = []

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
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.position[0], mouse_y - self.position[1]
        angle = math.atan2(rel_y, rel_x)
        speed = 10
        arrow = Arrow(self.position[0], self.position[1], angle, speed)
        self.arrows.append(arrow)

    def update_arrows(self, map):
        for arrow in self.arrows[:]:
            if arrow.update(map) or arrow.is_off_screen():
                self.arrows.remove(arrow)

    def draw_arrows(self, screen):
        for arrow in self.arrows:
            arrow.draw(screen)

# Класс противника
class Enemy:
    def __init__(self, x, y):
        self.position = [x * TILE_SIZE + TILE_SIZE/2, y * TILE_SIZE + TILE_SIZE/2]
        self.speed = 2
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x * TILE_SIZE + TILE_SIZE/2, y * TILE_SIZE + TILE_SIZE/2))
        self.vision_radius = 0  # Радиус обнаружения игрока

    def move_towards_player(self, player_position):
        dx = player_position[0] - self.position[0]
        dy = player_position[1] - self.position[1]
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance
        self.position[0] += dx * self.speed
        self.position[1] += dy * self.speed
        self.rect.center = self.position

    def can_see_player(self, player_position):
        dx = player_position[0] - self.position[0]
        dy = player_position[1] - self.position[1]
        distance = math.hypot(dx, dy)
        return distance <= self.vision_radius

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Класс тайла
class Tile:
    def __init__(self, tile_type: int):
        self.content = f'{tile_type}.png'
        self.image = pygame.image.load(self.content).convert_alpha()

# Класс карты
class Map:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.map = [[Tile(MAP[i][j]) for j in range(x)] for i in range(y)]

# Спавн противников
def spawn_enemies(map, count):
    enemies = []
    for _ in range(count):
        while True:
            x = random.randint(0, len(map[0]) - 1)
            y = random.randint(0, len(map) - 1)
            if MAP[y][x] == 0:
                enemies.append(Enemy(x, y))
                break
    return enemies

# Основной код
display = pygame.display.set_mode(flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()

play = Player('player_test.png', SPAWN)
karta = Map(len(MAP[0]), len(MAP))
enemies = spawn_enemies(MAP, 10)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            play.shoot()

    display.fill((220, 220, 220))

    # Отрисовка карты
    for i in range(len(MAP)):
        for j in range(len(MAP[0])):
            display.blit(karta.map[i][j].image, (j * TILE_SIZE, i * TILE_SIZE))

    # Обновление и отрисовка игрока
    play.rotate()
    play.move(karta.map)
    play.update_arrows(karta.map)
    play.draw_arrows(display)
    display.blit(play.image, play.rect)

    # Обновление и отрисовка противников
    for enemy in enemies:
        if enemy.can_see_player(play.position):
            enemy.move_towards_player(play.position)
        enemy.draw(display)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()