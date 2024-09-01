from typing import Tuple, List

from pygame import Rect

from Blocks import Block
from BlockSprites import BlockSprite
from FloorSprites import FloorSprite
from BoardSprites import BoardSprite
import pygame
import random


class ScoreBoard:

    def __init__(self, screen):
        self.screen = screen

        # Configuring fonts
        self.time_font = pygame.font.Font("Fonts/Asai-Analogue.ttf", 105)
        self.level_font = pygame.font.Font("Fonts/Asai-Analogue.ttf", 90)  # 115
        self.score_font = pygame.font.Font("Fonts/Asai-Analogue.ttf", 90)
        label_font = pygame.font.Font("Fonts/Time Won.otf", 25)
        label_outline_font = pygame.font.Font("Fonts/Time Won.otf", 27)

        # Initializing Score and Level values
        self.score = 5
        self.score_store = self.score
        self.total_score = 0
        self.level = 1
        self.total_time = 0

        # Initializing time, level, score and labels.
        self.time_text = self.time_font.render(f"{0:02}:{0:02}", True, "white")
        self.level_text = self.score_font.render(str(self.level), True, "white")  # Score number
        self.score_text = self.score_font.render(str(self.score), True, "white")  # Level number
        self.time_label = label_font.render("Time", True, "white")
        self.score_label = label_font.render("Score", True, "white")
        self.level_label = label_font.render("Level", True, "white")
        self.time_label_ol = label_outline_font.render("Time", True, "black")
        self.score_label_ol = label_outline_font.render("Score", True, "black")
        self.level_label_ol = label_outline_font.render("Level", True, "black")
        self.time_label_ol = label_outline_font.render("Time", True, "black")

        # Configuring Score Board
        self.outer_rim = pygame.rect.Rect(628, 0, 220, 220)
        self.inner_rim = pygame.rect.Rect(636, 8, 204, 204)
        self.div = pygame.rect.Rect(636, 104, 220, 8)
        self.time_div = pygame.rect.Rect(636, 28, 220, 6)
        self.vert_div = pygame.rect.Rect(734, 112, 8, 108)
        self.horiz_div = pygame.rect.Rect(636, 140, 204, 6)

    # Updates clock data
    def update_clock(self, total_seconds):
        seconds = total_seconds % 60
        minutes = total_seconds // 60
        self.total_time = total_seconds
        self.time_text = self.time_font.render(f"{minutes:02}:{seconds:02}", True, "white")

    # Updates score
    def update_score(self, score: int):
        self.score -= score
        self.total_score += score
        if self.score > 0:
            self.score_text = self.score_font.render(str(self.score), True, "white")
            self.screen.blit(self.score_text, (742 + (49 - (self.score_text.get_width() // 2)), 115))
            return
        else:
            return self.update_level(self.score)

    # Returns the total number of lines cleared..
    def get_total_score(self):
        return self.total_score

    # Returns the total seconds of gameplay
    def get_final_time(self):
        return self.total_time

    # Updates level and resets components associated with leveling
    def update_level(self, score: int):
        if score < 1:
            self.level += 1
            self.level_text = self.level_font.render(str(self.level), True, "white")
            self.score_store += 5
            self.score = self.score_store
            self.score_text = self.score_font.render(str(self.score), True, "white")
            return True
        raise Exception("Something's wrong with this...")

    # Draws the boundary blocks for the scoreboard
    def draw_score_boundary(self):
        screen = self.screen
        left_score_wall_x = 628
        left_score_wall_y = 0
        right_score_wall_x = 832
        right_score_wall_y = 0
        score_ceiling_x = 628
        score_ceiling_y = 0
        score_floor_x = 628
        score_floor_y = 204
        score_div_x = 628
        score_div_y = 102
        score_vert_div_x = 730
        score_vert_div_y = 102
        for i in range(7):
            pygame.draw.rect(screen, (59, 59, 59), (left_score_wall_x, left_score_wall_y, 34, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (left_score_wall_x + 30, left_score_wall_y + 4, 2, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (left_score_wall_x + 2, left_score_wall_y + 4, 2, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (left_score_wall_x + 4, left_score_wall_y + 30, 26, 2), 1, 8)
            pygame.draw.rect(screen, "black", (left_score_wall_x, left_score_wall_y, 34, 34), 1, 5)
            left_score_wall_y += 34
        for i in range(7):
            pygame.draw.rect(screen, (59, 59, 59), (right_score_wall_x, right_score_wall_y, 34, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (right_score_wall_x + 30, right_score_wall_y + 4, 2, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (right_score_wall_x + 2, right_score_wall_y + 4, 2, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (right_score_wall_x + 4, right_score_wall_y + 30, 26, 2), 1, 8)
            pygame.draw.rect(screen, "black", (right_score_wall_x, right_score_wall_y, 34, 34), 1, 5)
            right_score_wall_y += 34
        for i in range(7):
            pygame.draw.rect(screen, (59, 59, 59), (score_ceiling_x, score_ceiling_y, 34, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (score_ceiling_x + 30, score_ceiling_y + 4, 2, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (score_ceiling_x + 2, score_ceiling_y + 4, 2, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (score_ceiling_x + 4, score_ceiling_y + 30, 26, 2), 1, 8)
            pygame.draw.rect(screen, "black", (score_ceiling_x, score_ceiling_y, 34, 34), 1, 5)
            score_ceiling_x += 34
        for i in range(7):
            pygame.draw.rect(screen, (59, 59, 59), (score_floor_x, score_floor_y, 34, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (score_floor_x + 30, score_floor_y + 4, 2, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (score_floor_x + 2, score_floor_y + 4, 2, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (score_floor_x + 4, score_floor_y + 30, 26, 2), 1, 8)
            pygame.draw.rect(screen, "black", (score_floor_x, score_floor_y, 34, 34), 1, 5)
            score_floor_x += 34
        for i in range(7):
            pygame.draw.rect(screen, (59, 59, 59), (score_div_x, score_div_y, 34, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (score_div_x + 30, score_div_y + 4, 2, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (score_div_x + 2, score_div_y + 4, 2, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (score_div_x + 4, score_div_y + 30, 26, 2), 1, 8)
            pygame.draw.rect(screen, "black", (score_div_x, score_div_y, 34, 34), 1, 5)
            score_div_x += 34
        for i in range(3):
            pygame.draw.rect(screen, (59, 59, 59), (score_vert_div_x, score_vert_div_y, 34, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (score_vert_div_x + 30, score_vert_div_y + 4, 2, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (score_vert_div_x + 2, score_vert_div_y + 4, 2, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (score_vert_div_x + 4, score_vert_div_y + 30, 26, 2), 1, 8)
            pygame.draw.rect(screen, "black", (score_vert_div_x, score_vert_div_y, 34, 34), 1, 5)
            score_vert_div_y += 34

        left_queue_wall_x = 628
        left_queue_wall_y = 238
        right_queue_wall_x = 849
        right_queue_wall_y = 238
        queue_floor_x = 628
        queue_floor_y = 340
        for i in range(3):
            pygame.draw.rect(screen, (59, 59, 59), (left_queue_wall_x, left_queue_wall_y, 17, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (left_queue_wall_x + 15, left_queue_wall_y + 4, 1, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (left_queue_wall_x + 1, left_queue_wall_y + 4, 1, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (left_queue_wall_x + 2.125, left_queue_wall_y + 30, 13, 2), 1, 8)
            pygame.draw.rect(screen, "black", (left_queue_wall_x, left_queue_wall_y, 17, 34), 1, 5)
            left_queue_wall_y += 34
        for i in range(3):
            pygame.draw.rect(screen, (59, 59, 59), (right_queue_wall_x, right_queue_wall_y, 17, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (right_queue_wall_x + 15, right_queue_wall_y + 4, 1, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (right_queue_wall_x + 1, right_queue_wall_y + 4, 1, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (right_queue_wall_x + 2.125, right_queue_wall_y + 30, 13, 2), 1, 8)
            pygame.draw.rect(screen, "black", (right_queue_wall_x, right_queue_wall_y, 17, 34), 1, 5)
            right_queue_wall_y += 34
        for i in range(7):
            pygame.draw.rect(screen, (59, 59, 59), (queue_floor_x, queue_floor_y, 34, 34), 0, 5)
            pygame.draw.rect(screen, (112, 112, 112), (queue_floor_x + 30, queue_floor_y + 4, 2, 26), 0, 15)
            pygame.draw.rect(screen, (64, 64, 64), (queue_floor_x + 2, queue_floor_y + 4, 2, 26), 1, 8)
            pygame.draw.rect(screen, (10, 10, 10), (queue_floor_x + 4, queue_floor_y + 30, 26, 2), 1, 8)
            pygame.draw.rect(screen, "black", (queue_floor_x, queue_floor_y, 34, 34), 1, 5)
            queue_floor_x += 34

    # Draws scoreboard boundaries and data
    def draw_score_board(self):
        screen = self.screen
        self.draw_score_boundary()

        screen.blit(self.time_label, (662 + abs(85 - (self.time_label.get_width() / 2)), 7))
        screen.blit(self.time_text,(662 + abs(85 - (self.time_text.get_width() // 2)), abs(34 - (self.time_text.get_height() / 2))))
        screen.blit(self.level_text, (662 + 2 + (34 - (self.level_text.get_width() / 2)), 136 - 15))
        screen.blit(self.score_text, (764 + 3 + (34 - (self.score_text.get_width() / 2)), 136 - 15))
        screen.blit(self.level_label_ol, (662 + (34 - (self.level_label_ol.get_width() / 2)), 102 + (self.level_label_ol.get_height() - 20)))
        screen.blit(self.score_label_ol, (764 + (34 - (self.score_label_ol.get_width() / 2)), 102 + (self.score_label_ol.get_height() - 20)))
        screen.blit(self.level_label, (662 + (34 - (self.level_label.get_width() / 2)), 102 + (self.level_label.get_height() - 17)))
        screen.blit(self.score_label, (764 + (34 - (self.score_label.get_width() / 2)), 102 + (self.score_label.get_height() - 17)))
