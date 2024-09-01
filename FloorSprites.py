from typing import Tuple, List

from pygame import Rect

from Blocks import Block
from BlockSprites import BlockSprite
import pygame
import random

#from h import floored_blocks


class FloorSprite(pygame.sprite.Sprite):
    def __init__(self, block, color):
        super().__init__()
        # List of "floored" blocks
        self.floor_block = block

        # Variables holding value for each individual square in "block"
        self.rect1 = pygame.Rect(self.floor_block[0].x, self.floor_block[0].y, 34, 34)
        self.rect2 = pygame.Rect(self.floor_block[1].x, self.floor_block[1].y, 34, 34)
        self.rect3 = pygame.Rect(self.floor_block[2].x, self.floor_block[2].y, 34, 34)
        self.rect4 = pygame.Rect(self.floor_block[3].x, self.floor_block[3].y, 34, 34)
        self.floor_block = [self.rect1, self.rect2, self.rect3, self.rect4]
        # Holding the RBG color value associated with the block
        self.color = color

    # Returns an array of rect objects that comprise a "block"
    def get_floor_block(self):
        # len(self.floor_block)
        return self.floor_block

    # Returns a specific rect object from the "floor_block" list
    def get_rect(self, index):
        if -1 < index < len(self.floor_block):
            return self.floor_block[index]
        raise Exception(f"Index {index} out of range")


    # def get_lowest_y_by_x(self, falling_block_x):
    #     min_y = 748
    #     for floor_block in self.get_floor_block():
    #         if floor_block.x == falling_block_x:
    #             if min_y >= floor_block.y:
    #                 min_y = floor_block.y
    #     if min_y != 748:
    #         return min_y
    #     return min_y

    # Returns the color associated with the block
    def get_color(self):
        return self.color
