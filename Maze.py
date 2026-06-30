import pygame
import math
import time
import random
from PIL import Image
import numpy as np
random_start = random.randint(1, 3)
if random_start == 1:
    bild = Image.open("textures/Maze_1.png").convert("L")
elif random_start == 2:
    bild = Image.open("textures/Maze_2.png").convert("L")
elif random_start == 3:
    bild = Image.open("textures/Maze_3.png").convert("L")

pixels = np.array(bild)

World_map = []

for zeile in pixels:
    neue_zeile = []
    for pixel in zeile:
        if pixel == 0:
            neue_zeile.append(0)
        elif pixel == 255:
            neue_zeile.append(1) 
        else:
            neue_zeile.append(2)
    World_map.append(neue_zeile)





pygame.init()
WIN_HEIGHT = 1080
WIN_WIDHT = 1920
screen = pygame.display.set_mode((WIN_WIDHT, WIN_HEIGHT))
clock = pygame.time.Clock()
running = True
WALL_SIZE = WIN_HEIGHT * 1.0

MAX_BRIGHTNESS = 200
DIM_FACTOR = -15  

LINE_WITH = 3
NUMBER_OF_RAYS = int(WIN_WIDHT / LINE_WITH)
FOV = math.radians(75)
ANGLE_BETWEEN_RAYS = FOV / NUMBER_OF_RAYS

MOVE_SPEED = 0.01
Rotation_speed = math.radians(0.50)
PLAYER_RADIUS = 0.25  

def reset_game():
    return 10.5, 13.5, math.radians(random.randint(0, 360))

player_x, player_y, player_direction = reset_game()

FPS = 120
won = False

while running:
    clock.tick(FPS)
    pygame.display.set_caption(f"FPS: {int(clock.get_fps())} | Suche den goldene Block (2) auf der Map!")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    
    if not won:
        move_x = 0
        move_y = 0
        if keys[pygame.K_w]:
            move_x += math.cos(player_direction) * MOVE_SPEED
            move_y -= math.sin(player_direction) * MOVE_SPEED
        if keys[pygame.K_s]:
            move_x -= math.cos(player_direction) * MOVE_SPEED
            move_y += math.sin(player_direction) * MOVE_SPEED

        if keys[pygame.K_a]:
            move_x += math.cos(player_direction + math.pi/2) * MOVE_SPEED
            move_y -= math.sin(player_direction + math.pi/2) * MOVE_SPEED


        if keys[pygame.K_d]:
            move_x += math.cos(player_direction - math.pi/2) * MOVE_SPEED
            move_y -= math.sin(player_direction - math.pi/2) * MOVE_SPEED
        buffer_x = PLAYER_RADIUS if move_x > 0 else -PLAYER_RADIUS
        buffer_y = PLAYER_RADIUS if move_y > 0 else -PLAYER_RADIUS

        if move_x != 0 and World_map[int(player_y)][int(player_x + move_x + buffer_x)] != 1:
            player_x += move_x

        if move_y != 0 and World_map[int(player_y + move_y + buffer_y)][int(player_x)] != 1:
            player_y += move_y
        if keys[pygame.K_RIGHT]:
            player_direction = (player_direction - Rotation_speed) % (2 * math.pi)
        if keys[pygame.K_LEFT]:
            player_direction = (player_direction + Rotation_speed) % (2 * math.pi)
        
        if World_map[int(player_y)][int(player_x)] == 2 or \
           World_map[int(player_y + buffer_y)][int(player_x + buffer_x)] == 2:
            won = True
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (10, 10, 30), (0, 0, WIN_WIDHT, WIN_HEIGHT // 2))
    pygame.draw.rect(screen, (40, 25, 15), (0, WIN_HEIGHT // 2, WIN_WIDHT, WIN_HEIGHT // 2))


    ray_direction = player_direction + FOV / 2
    
    for i in range(NUMBER_OF_RAYS):
        ray_direction %= 2 * math.pi
        
        sin_a = math.sin(ray_direction)
        cos_a = math.cos(ray_direction)
        
        ray_y_dir = -sin_a 
        ray_x_dir = cos_a

        map_x = int(player_x)
        map_y = int(player_y)
        
        delta_dist_x = abs(1 / ray_x_dir) if ray_x_dir != 0 else 1e30
        delta_dist_y = abs(1 / ray_y_dir) if ray_y_dir != 0 else 1e30
        
        if ray_x_dir < 0:
            step_x = -1
            side_dist_x = (player_x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - player_x) * delta_dist_x

        if ray_y_dir < 0:
            step_y = -1
            side_dist_y = (player_y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - player_y) * delta_dist_y

        
        hit = False
        side = 0 
        hit_type = 0 
        
        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if World_map[map_y][map_x] > 0:
                hit_type = World_map[map_y][map_x]
                hit = True

        if side == 0:
            perp_wall_dist = side_dist_x - delta_dist_x
        else:
            perp_wall_dist = side_dist_y - delta_dist_y
            
        perp_wall_dist = max(0.01, perp_wall_dist)

        distance_without_fish_eye = perp_wall_dist * math.cos(player_direction - ray_direction)
        distance_without_fish_eye = max(0.05, distance_without_fish_eye) 

        line_height = WALL_SIZE / distance_without_fish_eye
        line_start = WIN_HEIGHT / 2 - line_height / 2

        
        brightness = int(DIM_FACTOR * distance_without_fish_eye + MAX_BRIGHTNESS)
        brightness = max(10, min(brightness, 255))
        if side == 1:
            brightness = int(brightness * 0.7)


        if hit_type == 2:

            color = (brightness, int(brightness * 0.8), 0)
        else:
            color = (brightness, brightness, brightness)
                
        line_screen_x = i * LINE_WITH
        pygame.draw.rect(screen, color, (line_screen_x, line_start, LINE_WITH, line_height))

        ray_direction -= ANGLE_BETWEEN_RAYS


    if won:
        font = pygame.font.SysFont("Arial", 64, bold=True)
        text = font.render("ZIEL ERREICHT! GEWONNEN!", True, (255, 215, 0))
        text_rect = text.get_rect(center=(WIN_WIDHT//2, WIN_HEIGHT//2))
        
        pygame.draw.rect(screen, (0,0,0), (text_rect.x - 20, text_rect.y - 10, text_rect.width + 40, text_rect.height + 20))
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        time.sleep(3)
        player_x, player_y, player_direction = reset_game()
        won = False
        continue

    pygame.display.flip()

pygame.quit()