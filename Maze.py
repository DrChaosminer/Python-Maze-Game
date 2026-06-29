import pygame
import math
World_map =  [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
pygame.init()
WIN_HEIGHT = 720
WIN_WIDHT = 1280
screen = pygame.display.set_mode((WIN_WIDHT, WIN_HEIGHT))
clock = pygame.time.Clock()
running = True
WALL_SIZE = WIN_HEIGHT * 1.1

MAX_BRIGHTNESS = 200
DIM_FACTOR = -5
#BLOCK_SIZE = WIN_HEIGHT / len(World_map)

# constant for raycasting
LINE_WITH = 1
NUMBER_OF_RAYS = int(WIN_WIDHT / LINE_WITH) + 1 
FOV = math.radians(60)
ANGLE_BETWEEN_RAYS = FOV / (NUMBER_OF_RAYS - 1)

#constant for the speed of the player
MOVE_SPEED = 0.06
Rotation_speed = math.radians(1.7)

#starting position of the player
player_x = 10.5
player_y = 13.5
player_direction = math.radians(252)

#We do not want the player to be on an exact integer position or have a direction of exactly 0.
# Occurrences of these events could result in glitches or division-by-zero errors.
# By adding a little starting offset to the values, we make
# these events extremely unlikely (practically impossible) to occur.
player_x += 0.00000001
player_y += 0.00000001
player_direction += 0.00000001

FPS =  60
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 50), (0, 0, WIN_WIDHT, WIN_HEIGHT / 2))
    pygame.draw.rect(screen, (65, 40, 20), (0, WIN_HEIGHT / 2, WIN_WIDHT, WIN_HEIGHT / 2))

    if keys[pygame.K_ESCAPE]:
        running = False
    
    #Move forward
    if keys[pygame.K_UP]:
        new_x = player_x + math.cos(player_direction) * MOVE_SPEED
        new_y = player_y -  math.sin(player_direction) * MOVE_SPEED
        if World_map[int(player_y)][int(new_x)] == 0:
            player_x = new_x
        if World_map[int(new_y)][int(player_x)] == 0:
            player_y = new_y



    #Move backwards
    if keys[pygame.K_DOWN]:        
        new_x = player_x - math.cos(player_direction) * MOVE_SPEED
        new_y = player_y +  math.sin(player_direction) * MOVE_SPEED
        if World_map[int(player_y)][int(new_x)] == 0:
            player_x = new_x
        if World_map[int(new_y)][int(player_x)] == 0:
            player_y = new_y

    #Spin right
    if keys[pygame.K_RIGHT]:
        player_direction -= Rotation_speed
        player_direction %= 2 * math.pi 
    #Spin Left
    if keys[pygame.K_LEFT]:
        player_direction += Rotation_speed
        player_direction %= 2 * math.pi 
    
    # Set Values to calculate the first ray 1111
    ray_direction = player_direction + FOV / 2
    ray_direction %= 2 * math.pi
    line_screen_x = 0

    cell_y = (player_y - math.floor(player_y)) 

    for i in range(NUMBER_OF_RAYS):

        # cell in which the ray is currently located
        ray_block_column = int(player_x)
        ray_block_row = int(player_y)

        ray_direction_degrees = math.degrees(ray_direction)

        if ray_direction_degrees > 0 and ray_direction_degrees < 180:
            next_horizontal_intersection_x = player_x + cell_y / math.tan(ray_direction)
            delta_x = 1 / math.tan(ray_direction)
            ray_row_movement = -1
        else:
            next_horizontal_intersection_x = player_x - (1 - cell_y) / math.tan(ray_direction)
            delta_x = -1 / math.tan(ray_direction)
            ray_row_movement = 1

        # ... Make all the calculations for the raycasting here ...
        if  (ray_direction_degrees > 270 and ray_direction_degrees < 90):
            next_vertical_intersection_x = math.ceil(player_x)
            ray_column_movement = 1
        else:
            next_vertical_intersection_x = math.floor(player_x)
            ray_column_movement = -1

        while True:
            distance_horizontal_intersection = abs(player_x - next_horizontal_intersection_x)
            distance_vertical_intersection = abs(player_x - next_vertical_intersection_x) 
            if distance_horizontal_intersection < distance_vertical_intersection:
                current_ray_x = next_horizontal_intersection_x
                ray_block_row += ray_row_movement 
                next_horizontal_intersection_x += delta_x
            else:
                current_ray_x = next_vertical_intersection_x
                ray_block_column += ray_column_movement
                next_vertical_intersection_x += ray_column_movement


            if World_map[ray_block_row][ray_block_column] == 1:
                break
        
        raw_distance = (current_ray_x - player_x) / math.cos(ray_direction)
        distance_without_fish_eye = raw_distance * math.cos(player_direction - ray_direction)

        line_height = WALL_SIZE / distance_without_fish_eye
        line_start = WIN_HEIGHT / 2 - line_height / 2
        line__start = max(line_start, 0)
        line_end = WIN_HEIGHT / 2 + line_height / 2
        line_end = min(line_end, WIN_HEIGHT)

        
        brighness = int(DIM_FACTOR * distance_without_fish_eye + MAX_BRIGHTNESS)
        brighness = max(brighness, 0)
        brighness = min(brighness, 255)

        pygame.draw.line(screen, (0, brighness, 0), (line_screen_x, line_start), (line_screen_x, line_end), LINE_WITH)

        ray_direction -= ANGLE_BETWEEN_RAYS
        ray_direction %= 2 * math.pi
        line_screen_x += LINE_WITH


    pygame.display.flip()
"""
    for row in range(len(World_map)):
        for col in range(len(World_map[row])):
            if World_map[row][col] == 1:
                pygame.draw.rect(screen, (0, 200, 0), (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            else:
                pygame.draw.rect(screen, (255,255,255), (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    player_screen_x = player_x * BLOCK_SIZE
    player_screen_y = player_y * BLOCK_SIZE
    pygame.draw.circle(screen, (255, 0, 0), (int(player_screen_x), int(player_screen_y)), int(BLOCK_SIZE / 5))
"""

        