from typing import Tuple, List

from pygame import Rect

from Blocks import Block
from BlockSprites import BlockSprite
from FloorSprites import FloorSprite
from BoardSprites import BoardSprite
from ScoreBoard_ import ScoreBoard
import pygame
import random



class HitMap:
    def __init__(self, floor_block: list[FloorSprite]):
        self.map = {
            254: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            288: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            322: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            356: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            390: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            424: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            458: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            492: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            526: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            560: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            594: [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True],
            }

        self.floor_block = floor_block

    # Sets the hit map with positions of floor block rects
    def set_map(self):
        for floor in self.floor_block:
            for i, f in enumerate(floor.get_floor_block()):
                save_rect = floor.get_rect(i)
                save_rect_x = save_rect.x
                save_rect_y = (save_rect.y / 34) - 1

                change_bool = self.map[save_rect_x]
                change_bool[int(save_rect_y)] = True

    # Returns the "Hit Map" dictionary
    def get_map(self):
        return self.map

    # Detects if a falling block's rects have reached a position logged in the "Hit Map"
    # And returns rect positions one unit higher than a logged position
    def find_hit(self, block: list[Rect]):
        for i in range(20):
            rect1 = block[0]
            rect2 = block[1]
            rect3 = block[2]
            rect4 = block[3]

            rect1_x = rect1.x
            rect2_x = rect2.x
            rect3_x = rect3.x
            rect4_x = rect4.x

            rect1_y = rect1.y / 34 - 1
            rect2_y = rect2.y / 34 - 1
            rect3_y = rect3.y / 34 - 1
            rect4_y = rect4.y / 34 - 1

            bool1 = self.map[int(rect1_x)][int(rect1_y)]
            bool2 = self.map[int(rect2_x)][int(rect2_y)]
            bool3 = self.map[int(rect3_x)][int(rect3_y)]
            bool4 = self.map[int(rect4_x)][int(rect4_y)]

            if not bool1 and not bool2 and not bool3 and not bool4:
                block[0].y += 34
                block[1].y += 34
                block[2].y += 34
                block[3].y += 34
            else:
                block[0].y -= 34
                block[1].y -= 34
                block[2].y -= 34
                block[3].y -= 34
                return [block[0], block[1], block[2], block[3]]

    # Finds the lowest logged position in the HitMap returns rect positions one unit higher than a logged position
    # for Falling block outline
    def find_floor(self, block: list[Rect]):
        for i in range(20):
            rect1 = block[0]
            rect2 = block[1]
            rect3 = block[2]
            rect4 = block[3]

            rect1_x = rect1.x
            rect2_x = rect2.x
            rect3_x = rect3.x
            rect4_x = rect4.x

            rect1_y = rect1.y / 34 - 1
            rect2_y = rect2.y / 34 - 1
            rect3_y = rect3.y / 34 - 1
            rect4_y = rect4.y / 34 - 1

            bool1 = self.map[int(rect1_x)][int(rect1_y)]
            bool2 = self.map[int(rect2_x)][int(rect2_y)]
            bool3 = self.map[int(rect3_x)][int(rect3_y)]
            bool4 = self.map[int(rect4_x)][int(rect4_y)]

            if not bool1 and not bool2 and not bool3 and not bool4:
                block[0].y += 34
                block[1].y += 34
                block[2].y += 34
                block[3].y += 34
            else:
                block[0].y -= 34
                block[1].y -= 34
                block[2].y -= 34
                block[3].y -= 34
                return [block[0], block[1], block[2], block[3]]

    # Checks if values have been registered for the rects beneath a rect
    def collide_check(self, block: list[Rect]):
        for i in range(1):
            rect1 = block[0]
            rect2 = block[1]
            rect3 = block[2]
            rect4 = block[3]

            rect1_x = rect1.x
            rect2_x = rect2.x
            rect3_x = rect3.x
            rect4_x = rect4.x

            rect1_y = rect1.y / 34
            rect2_y = rect2.y / 34
            rect3_y = rect3.y / 34
            rect4_y = rect4.y / 34

            bool1 = self.map[int(rect1_x)][int(rect1_y)]
            bool2 = self.map[int(rect2_x)][int(rect2_y)]
            bool3 = self.map[int(rect3_x)][int(rect3_y)]
            bool4 = self.map[int(rect4_x)][int(rect4_y)]

            if not bool1 and not bool2 and not bool3 and not bool4:
                block[0].y += 34
                block[1].y += 34
                block[2].y += 34
                block[3].y += 34
                return [block[0], block[1], block[2], block[3]]

            else:
                return None
