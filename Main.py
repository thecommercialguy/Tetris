# Example file showing a circle moving on screen
from typing import Tuple, List

from pygame import Rect

from Blocks import Block
from BlockSprites import BlockSprite
from FloorSprites import FloorSprite
from BoardSprites import BoardSprite
from ScoreBoard_ import ScoreBoard
from HitMap_ import HitMap
from BlockQueue_ import BlockQueue
import pygame
import random


def add_to_floor(block: List[Rect]):
    for b in block:
        floored_blocks.append(b)


# def add_to_floorS(block):
#     floored_blocks.append(block)


def floor_add(block, floor):
    for i, r in enumerate(block):
        collision_index = r.collidelist(floor)
        if collision_index != -1:
            add_to_floor(block)
            current_block.delete_blocks()
            cnt = 0


# def floor_block_collide(block_sprite, floor_blocks) -> bool:
#
#     for r in block_sprite.rects:
#         for floor in floor_blocks:
#             collision_index = r.collidelist(floor.get_floor_block())
#             if collision_index != -1:
#                 # add_to_floor(current_block.rects)
#                 floored_block = FloorSprite(block_sprite.rects, block_sprite.color)
#                 floored_blocks1.append(floored_block)
#                 block_sprite.delete_blocks()
#                 return True
#             #cnt = 0
#     return False

# Drops positions of floor blocks by a single unit (34) above a rect
def drop_floor(floor: list[FloorSprite], y_values):
    for f in floor:
        block = f.get_floor_block()
        for b in block:
            for y in y_values:  # rough estimate, may change
                if b.y < y:
                    b.y += 34


# Method to sort the y-values of each row set to be cleared
def sort_row(rows) -> list[int]:
    if len(rows) > 1:
        sorted_y = []
        for r in rows:
            sorted_y.append(r.y)
        sorted_y.sort()

        return sorted_y

    return [rows[-1].y]

# Runs a clearing animation at the y-position of each row to be cleared
def clear_animation(y_values: list[int], i: int):
    if i == 0:
        clear_config(y_values[i])
        return

    clear_config(y_values[i])

    i -= 1
    return clear_animation(y_values, i)

# Configures the clearing animation at the y-position of each row to be cleared
def clear_config(y_value: int):
    # temp_surface = pygame.Surface((848,748), pygame.SRCALPHA)
    wide = pygame.Rect(254, y_value, 340, 34)
    medium = pygame.Rect(254 + ((340/2)-((340/3)*2)/2), y_value, (340//3)*2, 34)
    small = pygame.Rect(254 + ((340/2)-(340/3)/2), y_value, 340//3, 34)


    pygame.draw.rect(screen, "white", small, 0, 4)
    pygame.display.flip()
    pygame.time.delay(150)
    pygame.draw.rect(screen, "purple", medium, 0, 4)
    pygame.display.flip()
    pygame.time.delay(150)
    pygame.draw.rect(screen, "green", wide, 0, 4)
    pygame.display.flip()
    pygame.time.delay(150)

# Draws a copy of the most recent falling block to maintain its image while clearing
def draw_temp_block(color, block):
    #print(block)
    if block:
        for i in range(len(block)):
            pygame.draw.rect(screen, color, block[i], 0, 4)
            pygame.draw.rect(screen, "white", (block[i].x + 30, block[i].y + 4, 2, 26), 0, 15)
            pygame.draw.rect(screen, color_dict[color][0],
                             (block[i].x + 2, block[i].y + 4, 2, 26), 1, 8)
            pygame.draw.rect(screen, color_dict[color][1],
                             (block[i].x + 4, block[i].y + 30, 26, 2), 1, 8)
            pygame.draw.rect(screen, "black", block[i], 1, 4)

# Draws the game's borders
def draw_border():
    screen.fill("black")
    ceiling_x = 220
    ceiling_y = 0
    right_wall_x = 220
    right_wall_y = 0
    left_wall_x = 594
    left_wall_y = 0
    floor_x = 220
    floor_y = 714
    for i in range(12):
        pygame.draw.rect(screen, (59, 59, 59), (ceiling_x, ceiling_y, 34, 34), 0, 5)
        pygame.draw.rect(screen, (112, 112, 112), (ceiling_x + 30, ceiling_y + 4, 2, 26), 0, 15)
        pygame.draw.rect(screen, (64, 64, 64), (ceiling_x + 2, ceiling_y + 4, 2, 26), 1, 8)
        pygame.draw.rect(screen, (10, 10, 10), (ceiling_x + 4, ceiling_y + 30, 26, 2), 1, 8)
        pygame.draw.rect(screen, "black", (ceiling_x, ceiling_y, 34, 34), 1, 5)
        ceiling_x += 34
    for i in range(22):
        pygame.draw.rect(screen, (59, 59, 59), (right_wall_x, right_wall_y, 34, 34), 0, 5)
        pygame.draw.rect(screen, (112, 112, 112), (right_wall_x + 30, right_wall_y + 4, 2, 26), 0, 15)
        pygame.draw.rect(screen, (64, 64, 64), (right_wall_x + 2, right_wall_y + 4, 2, 26), 1, 8)
        pygame.draw.rect(screen, (10, 10, 10), (right_wall_x + 4, right_wall_y + 30, 26, 2), 1, 8)
        pygame.draw.rect(screen, "black", (right_wall_x, right_wall_y, 34, 34), 1, 5)
        right_wall_y += 34
    for i in range(22):
        pygame.draw.rect(screen, (59, 59, 59), (left_wall_x, left_wall_y, 34, 34), 0, 5)
        pygame.draw.rect(screen, (112, 112, 112), (left_wall_x + 30, left_wall_y + 4, 2, 26), 0, 15)
        pygame.draw.rect(screen, (64, 64, 64), (left_wall_x + 2, left_wall_y + 4, 2, 26), 1, 8)
        pygame.draw.rect(screen, (10, 10, 10), (left_wall_x + 4, left_wall_y + 30, 26, 2), 1, 8)
        pygame.draw.rect(screen, "black", (left_wall_x, left_wall_y, 34, 34), 1, 5)
        left_wall_y += 34
    for i in range(12):
        pygame.draw.rect(screen, (59, 59, 59), (floor_x, floor_y, 34, 34), 0, 5)
        pygame.draw.rect(screen, (112, 112, 112), (floor_x + 30, floor_y + 4, 2, 26), 0, 15)
        pygame.draw.rect(screen, (64, 64, 64), (floor_x + 2, floor_y + 4, 2, 26), 1, 8)
        pygame.draw.rect(screen, (10, 10, 10), (floor_x + 4, floor_y + 30, 26, 2), 1, 8)
        pygame.draw.rect(screen, "black", (floor_x, floor_y, 34, 34), 1, 5)
        floor_x += 34

# Returns True if end game conditions are met
def end_game_conditions_check(map) -> bool:
    if map[390][1] or map[424][1]:
        return True
    return False

# Method that displays the endgame animation, including "GAMEOVER," the total lines cleared, and total time of gameplay
def end_game_animation():
    # Drawing endgame background color
    pygame.draw.rect(screen, "white", (254 + (170 - (4 * 34)), 4 * 34, 8 * 34, 4 * 34))

    # Drawing endgame border
    game_over_left_wall_x = 272
    game_over_left_wall_y = 3 * 34
    game_over_ceiling_x = 306
    game_over_ceiling_y = 3 * 34
    game_over_right_wall_x = 272 + 34 * 8
    game_over_right_wall_y = 3 * 34
    game_over_floor_x = 272
    game_over_floor_y = 3 * 34 + 5 * 34

    for i in range(6):
        pygame.draw.rect(screen, (59, 59, 59), (game_over_left_wall_x, game_over_left_wall_y, 34, 34), 0, 5)
        pygame.draw.rect(screen, (112, 112, 112), (game_over_left_wall_x + 30, game_over_left_wall_y + 4, 2, 26), 0, 15)
        pygame.draw.rect(screen, (64, 64, 64), (game_over_left_wall_x + 2, game_over_left_wall_y + 4, 2, 26), 1, 8)
        pygame.draw.rect(screen, (10, 10, 10), (game_over_left_wall_x + 4, game_over_left_wall_y + 30, 26, 2), 1, 8)
        pygame.draw.rect(screen, "black", (game_over_left_wall_x, game_over_left_wall_y, 34, 34), 1, 5)
        game_over_left_wall_y += 34

    for i in range(8):
        pygame.draw.rect(screen, (59, 59, 59), (game_over_ceiling_x, game_over_ceiling_y, 34, 34), 0, 5)
        pygame.draw.rect(screen, (112, 112, 112), (game_over_ceiling_x + 30, game_over_ceiling_y + 4, 2, 26), 0, 15)
        pygame.draw.rect(screen, (64, 64, 64), (game_over_ceiling_x + 2, game_over_ceiling_y + 4, 2, 26), 1, 8)
        pygame.draw.rect(screen, (10, 10, 10), (game_over_ceiling_x + 4, game_over_ceiling_y + 30, 26, 2), 1, 8)
        pygame.draw.rect(screen, "black", (game_over_ceiling_x, game_over_ceiling_y, 34, 34), 1, 5)
        game_over_ceiling_x += 34
    for i in range(6):
        pygame.draw.rect(screen, (59, 59, 59), (game_over_right_wall_x, game_over_right_wall_y, 34, 34), 0, 5)
        pygame.draw.rect(screen, (112, 112, 112), (game_over_right_wall_x + 30, game_over_right_wall_y + 4, 2, 26), 0,
                         15)
        pygame.draw.rect(screen, (64, 64, 64), (game_over_right_wall_x + 2, game_over_right_wall_y + 4, 2, 26), 1, 8)
        pygame.draw.rect(screen, (10, 10, 10), (game_over_right_wall_x + 4, game_over_right_wall_y + 30, 26, 2), 1, 8)
        pygame.draw.rect(screen, "black", (game_over_right_wall_x, game_over_right_wall_y, 34, 34), 1, 5)
        game_over_right_wall_y += 34
    for i in range(8):
        pygame.draw.rect(screen, (59, 59, 59), (game_over_floor_x, game_over_floor_y, 34, 34), 0, 5)
        pygame.draw.rect(screen, (112, 112, 112), (game_over_floor_x + 30, game_over_floor_y + 4, 2, 26), 0, 15)
        pygame.draw.rect(screen, (64, 64, 64), (game_over_floor_x + 2, game_over_floor_y + 4, 2, 26), 1, 8)
        pygame.draw.rect(screen, (10, 10, 10), (game_over_floor_x + 4, game_over_floor_y + 30, 26, 2), 1, 8)
        pygame.draw.rect(screen, "black", (game_over_floor_x, game_over_floor_y, 34, 34), 1, 5)
        game_over_floor_x += 34

    # Obtaining the last clock tick prior to the game ending
    final_time = score_board.get_final_time()
    seconds = final_time % 60
    minutes = final_time // 60

    # Initializing fonts for endgame text
    game_over_font = pygame.font.Font("Fonts/Time Won.otf", 100)
    game_over_font1 = pygame.font.Font("Fonts/Time Won.otf", 75)
    game_over_font2 = pygame.font.Font("Fonts/Time Won.otf", 52)
    game_over_font3 = pygame.font.Font("Fonts/Time Won.otf", 40)
    final_score_font = pygame.font.Font("Fonts/Asai-Analogue.ttf", 45)
    final_time_font = pygame.font.Font("Fonts/Asai-Analogue.ttf", 45)
    final_label_font = pygame.font.Font("Fonts/Time Won.otf", 30)

    # Initializing text to display
    game_over_text = game_over_font.render("GAME OVER", True, "blue")
    game_over_text1 = game_over_font1.render("GAME OVER", True, "yellow")
    game_over_text2 = game_over_font2.render("GAME OVER", True, "green")
    game_over_text3 = game_over_font3.render("GAME OVER", True, "red")
    final_score_text = final_score_font.render(str(score_board.get_total_score()), True, "green")
    final_time_text = final_time_font.render(f"{minutes:02}:{seconds:02}", True, "green")
    final_score_label = final_label_font.render("Lines", True, "black")
    final_time_label = final_label_font.render("Time", True, "black")

    # Incrementing display changes based on the seconds following GAMEOVER(line #) being set to true
    post_tick_1 = final_time + 1
    post_tick_2 = post_tick_1 + 1
    post_tick_3 = post_tick_2 + 1
    post_tick_4 = post_tick_3 + 1

    # Displays "GAMEOVER_TEXT" (LARGER)
    if total_seconds == final_time:
        screen.blit(game_over_text, (
            0 + (424 - game_over_text.get_width() // 2),
            ((5 * 34) - game_over_text3.get_height() // 2)))

    # Displays "GAMEOVER_TEXT" (MEDIUM)
    if total_seconds == post_tick_1:
        screen.blit(game_over_text1, (
            (0 + (424 - game_over_text1.get_width() // 2)),
            ((5 * 34) - game_over_text3.get_height() // 2)))

    # Displays "GAMEOVER_TEXT" (SMALL)
    if total_seconds == post_tick_2:
        screen.blit(game_over_text2, (
            (0 + (424 - game_over_text2.get_width() // 2)),
            ((5 * 34) - game_over_text3.get_height() // 2)))

    # Displays "GAMEOVER_TEXT" (SMALLER)
    if total_seconds >= post_tick_3:

        screen.blit(game_over_text3, (
            (272 + 34 + (119 - game_over_text3.get_width() / 2)),
            ((5 * 34) - game_over_text3.get_height() // 2)))

        # Displays final score and time along with their labels
        if total_seconds >= post_tick_4:
            screen.blit(final_score_label, (
                (306 + (59.5 - final_score_label.get_width() / 2)),
                ((6 * 34) + 10 - game_over_text3.get_height() // 2)))
            screen.blit(final_score_text, (
                (306 + (59.5 - final_score_text.get_width() / 2)),
                ((6 * 34) + 30 - game_over_text3.get_height() // 2)))
            screen.blit(final_time_label, (
                (425 + (59.5 - final_time_label.get_width() / 2)),
                ((6 * 34) + 10 - game_over_text3.get_height() // 2)))
            screen.blit(final_time_text, (
                (425 + (59.5 - final_time_text.get_width() / 2)),
                ((6 * 34) + 30 - game_over_text3.get_height() // 2)))


# Dictionary containing "shades" associated with each block's primary color
color_dict = {
    # main color: [ left side color, bottom color]
    (252, 93, 178): [(252, 93, 178), (235, 14, 154)],
    (237, 123, 9): [(237, 96, 2), (191, 98, 6)],
    (255, 247, 3): [(252, 215, 50), (189, 183, 19)],
    (232, 12, 12): [(166, 7, 7), (209, 33, 33)],
    (131, 54, 135): [(138, 76, 158), (105, 36, 110)],
    (78, 135, 79): [(83, 120, 78), (48, 84, 49)],
    (133, 235, 242): [(132, 221, 227), (76, 160, 166)]
}
# pygame setup
pygame.init()
screen = pygame.display.set_mode((866, 748))  #848
clock = pygame.time.Clock()
running = True
dt = 0
v = 300
# x = 200
# y = 400
# sp = pygame.sprite.Sprite
# A "HitMap" object to initialize first falling block
open = HitMap([])

bb = Block()

# Initializing score board
score_board = ScoreBoard(screen)

dev_mode = False

# Initializing block queue
block_queue = BlockQueue(bb, color_dict, screen)
block_queue.set_queue_blocks()

# Setting the first falling "block" and obtaining its associated data
index = random.randint(0, 6)
new_block = bb.blocks[index]

# Obtains the shape ID for the block
block_shape = new_block[1]

# Initializing block sprite object with the newly selected block's data
current_block = BlockSprite(new_block, [], open)

#counter = [0, 1, 2, 3]
# Initializing "count" used for block rotation (line #)
cnt = 0


floored_blocks = []
# Contains list of "FloorSprites"
floored_blocks1 = []

# Initializing timer
total_seconds = 0
font = pygame.font.Font(None, 100)
start_ticks = pygame.time.get_ticks()
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)

# Initializing value to store "HitMap" data (line #)
map = None

# A numerical indicator differentiating "Snap to floor" methods (line #)
switch = 0

# Used to "lock" rotation functionality once block has met conditions to be
# added to floor
lock = False

# Indicating if end game conditions have been met
on = True


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Block controls
            elif event.type == pygame.KEYDOWN and on:
                # "Snaps" a block to the floor
                if event.key == pygame.K_w:
                    if len(floored_blocks1) > 0:
                        current_block.snap_to_floor_()
                        switch = 2
                    else:
                        snap = current_block.snap_to_floor()
                        switch = 1
                # Moves block to the left
                elif event.key == pygame.K_a and on:
                    shift = -34
                    if not current_block.left_right_collide(shift, floored_blocks1):
                        current_block.move_left()
                # Drops block by a single unit (+34)
                elif event.key == pygame.K_s and on:
                    current_block.block_decent_by_unit()
                # Moves block to the right
                elif event.key == pygame.K_d and on:
                    shift = 34
                    if not current_block.left_right_collide(shift, floored_blocks1):
                        current_block.move_right()
                # Rotates the block
                elif event.key == pygame.K_SPACE and not lock:
                    if cnt < 4:
                        print(current_block.rects, "at")
                        print(f"#####{cnt}#####")
                        if current_block.rotate(cnt):
                            cnt += 1

                    else:
                        cnt = 0
                        if current_block.rotate(cnt):
                            cnt += 1

            elif event.type == timer_event:

                total_seconds += 1

                if on:
                    blok = current_block.rects
                    col = current_block.color

                    # Contains the logic for a block falling,
                    # the creation of a new block, the addition of the "stopped" block to
                    # the "floored blocks" list, and logic for determining completed rows.

                    if switch == 2 or not current_block.block_fall_collision_check(floored_blocks1):
                        lock = True
                        index = block_queue.dequeue_block()
                        new_block = bb.blocks[index]
                        block_queue.push_queue_block()
                        floor_block = FloorSprite(blok, col)
                        floored_blocks1.append(floor_block)
                        hit_update = HitMap(floored_blocks1)
                        hit_update.set_map()
                        map = hit_update.map
                        temp_block = floor_block.get_floor_block()
                        temp_block_by_index = [temp_block[0], temp_block[1], temp_block[2], temp_block[3]]
                        board = BoardSprite(floored_blocks1)
                        var = board.if_collide()
                        if var[-1] != 'clear':
                            board.selection(var)
                            y_values = sort_row(var)
                            draw_temp_block(col, temp_block_by_index)
                            pygame.display.flip()
                            clear_animation(y_values, len(y_values) - 1)
                            score_board.update_score(len(y_values))
                            drop_floor(floored_blocks1, y_values)
                        hit_update = HitMap(floored_blocks1)
                        hit_update.set_map()
                        map = hit_update.map
                        cnt = 0
                        switch = 0
                        lock = False
                        if current_block.delete_blocks():
                            if on:
                                current_block.__init__(new_block, floored_blocks1, hit_update)

                    # Contains the logic for a block falling,
                    # the creation of a new block, the addition of the "stopped" block to
                    # the "floored blocks" list, and logic for determining completed rows.

                    if switch == 1 or not current_block.block_descent():
                        lock = True
                        index = block_queue.dequeue_block()
                        new_block = bb.blocks[index]
                        block_queue.push_queue_block()
                        add_to_floor(current_block.rects)
                        floor_block = FloorSprite(blok, col)
                        temp_block = floor_block.get_floor_block()
                        temp_block_by_index = [temp_block[0], temp_block[1], temp_block[2], temp_block[3]]
                        floored_blocks1.append(floor_block)
                        board = BoardSprite(floored_blocks1)
                        row = board.if_collide()
                        if row[-1] != 'clear':
                            board.selection(row)
                            y_values = sort_row(row)
                            draw_temp_block(col, temp_block_by_index)
                            pygame.display.flip()
                            clear_animation(y_values, len(y_values) - 1)
                            score_board.update_score(len(y_values))
                            drop_floor(floored_blocks1, y_values)
                        hit_update = HitMap(floored_blocks1)
                        hit_update.set_map()
                        map = hit_update.map
                        cnt = 0
                        switch = 0
                        lock = False
                        if current_block.delete_blocks():
                            if on:
                                current_block.__init__(new_block, floored_blocks1, hit_update)

    # Updates clock while endgame conditions haven't been met
    if on:
        score_board.update_clock(total_seconds)

    draw_border()

    score_board.draw_score_board()


    if len(current_block.rects) > 0:


        # Draws blocks that have been "floored"
        if len(floored_blocks1) > 0:
            for block in floored_blocks1:
                i = 0
                while i < len(block.get_floor_block()):
                    pygame.draw.rect(screen, block.get_color(), block.get_rect(i),0,4)
                    pygame.draw.rect(screen, color_dict[block.get_color()][0], (block.get_rect(i).x + 2, block.get_rect(i).y + 4, 2, 26), 1, 8)
                    pygame.draw.rect(screen, color_dict[block.get_color()][1], (block.get_rect(i).x + 4, block.get_rect(i).y + 30, 26, 2), 1, 8)
                    pygame.draw.rect(screen, "white", (block.get_rect(i).x+30,block.get_rect(i).y+4,2,26), 0, 15)
                    pygame.draw.rect(screen, "black", block.get_rect(i), 1, 4)

                    i += 1

        if on:
            # Draws the outline of the falling block along the floor or floored blocks directly beneath it
            outline = current_block.floor_outline()
            outline_color = current_block.get_color()

            for skel in outline:
                pygame.draw.rect(screen, outline_color, skel, 2, 4)

            # Draws the "rect" objects that comprise the falling / current block
            if len(current_block.rects) > 0:
                for rect in current_block.rects:

                    pygame.draw.rect(screen, current_block.color, rect, 0, 4)
                    pygame.draw.rect(screen, "white", (rect.x+30,rect.y+4,2,26), 1, 8)
                    pygame.draw.rect(screen, color_dict[current_block.color][0], (rect.x + 2, rect.y + 4, 2, 26), 1, 8)
                    pygame.draw.rect(screen, color_dict[current_block.color][1], (rect.x + 4, rect.y + 30, 26, 2), 1, 8)
                    pygame.draw.rect(screen, "black", rect, 1, 4)

    # Draws block queue and surrounding borders
    block_queue.draw_queue_blocks()

    # Begins checking for endgame conditions once map is initialized
    if map is not None:
        # Checks if endgame conditions have been met
        if end_game_conditions_check(map):
            on = False
            pygame.time.delay(500)
            current_block.delete_blocks()
            end_game_animation()

            for blo in floored_blocks1:
                for bl in blo.get_floor_block():
                    bl.y += 34




    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    # Straight up deleting floor blocks?


pygame.quit()

