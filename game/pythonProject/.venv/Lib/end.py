import random
import math
import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
TILE_SIZE = 64
SPAWN = [2, 2]
MAP = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#[
#    [2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [2, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [2, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
#    [2, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [2, 2, 2, 2, 2, 0, 0, 2, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
#    [2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
#    [2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 1, 1, 1, 2],
#    [2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1, 2],
#    [2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1, 1, 1, 2],
#    [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2],
#]

X = len(MAP[0])
Y = len(MAP)


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
            self.health = min(100, self.health + 0.05)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        self.last_damage_time = pygame.time.get_ticks()

    def draw_health(self, screen):
        pass
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, 2 * self.health, 20))

class Enemy:
    def __init__(self, x, y):
        self.position = [x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2]
        self.speed = 100
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2))
        self.vision_radius = 50
        self.health = 3
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


class Tile:
    def __init__(self, tile_type: int):
        self.content = f'{tile_type}.png'
        self.image = pygame.image.load(self.content).convert_alpha()


class Map:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.map = [[Tile(MAP[i][j]) for j in range(x)] for i in range(y)]

def spawn_enemies(map, count):
    enemies = []
    occupied_tiles = set()
    for _ in range(count):
        while True:
            x = random.randint(0, len(map[0]) - 1)
            y = random.randint(0, len(map) - 1)
            if MAP[y][x] == 0 and (x, y) not in occupied_tiles:
                enemies.append(Enemy(x, y))
                occupied_tiles.add((x, y))
                break
    return enemies


# Основной код
display = pygame.display.set_mode(flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()

play = Player('player_test.png', SPAWN)
karta = Map(len(MAP[0]), len(MAP))
enemies = spawn_enemies(MAP, 250)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            play.shoot()

    display.fill((220, 220, 220))

    for i in range(len(MAP)):
        for j in range(len(MAP[0])):
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

    pygame.display.flip()
    clock.tick(FPS)

font = pygame.font.Font(None, 36)

pygame.quit()
