from typing import Tuple, List

from pygame import Rect

from Blocks import Block
from BlockSprites import BlockSprite
from FloorSprites import FloorSprite
import pygame
import random

class BoardSprite(pygame.sprite.Sprite):
    _floor: FloorSprite
    _blocks: list[FloorSprite]

    def __init__(self, blocks: list[FloorSprite]):
        super().__init__()


        self._blocks = blocks

        row1 = pygame.Rect(340, 34, 34, 34)
        row2 = pygame.Rect(340, 68, 34, 34)
        row3 = pygame.Rect(340, 102, 34, 34)
        row4 = pygame.Rect(340, 136, 34, 34)
        row5 = pygame.Rect(340, 170, 34, 34)
        row6 = pygame.Rect(340, 204, 34, 34)
        row7 = pygame.Rect(340, 238, 34, 34)
        row8 = pygame.Rect(340, 272, 34, 34)
        row9 = pygame.Rect(340, 306, 34, 34)
        row10 = pygame.Rect(340, 340, 34, 34)
        row11 = pygame.Rect(340, 374, 34, 34)
        row12 = pygame.Rect(340, 408, 34, 34)
        row13 = pygame.Rect(340, 442, 34, 34)
        row14 = pygame.Rect(340, 476, 34, 34)
        row15 = pygame.Rect(340, 510, 34, 34)
        row16 = pygame.Rect(340, 544, 34, 34)
        row17 = pygame.Rect(340, 578, 34, 34)
        row18 = pygame.Rect(340, 612, 34, 34)
        row19 = pygame.Rect(340, 646, 34, 34)
        self.row20 = pygame.Rect(340, 680, 34, 34)
        self.rows = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12, row13, row14, row15,
                     row16, row17, row18, row19, self.row20]

    # Determines
    def if_collide(self):
        # A register of rects with equal y-values
        reg = []
        if len(self._blocks) > 1:
            for r in self.rows:
                cnt = 0
                for b in self._blocks:
                    for i, bl in enumerate(b.get_floor_block()):

                        val = b.get_rect(i)

                        if r.y == val.y:
                            cnt += 1

                if cnt == 10:
                    print("OKAY THAT'S THE ROW")
                    reg.append(r)

        # Returns the rects comprising a completed row
        if len(reg) > 0:
            return reg
        # Indicator the no row is "complete"
        return ['clear']

    # Removing rects with y-values within a completed row
    def selection(self, reg):
        if reg[-1] == 'clear':
            return
        dele = []


        for r in reg:
            for b in self._blocks:
                var = b.get_floor_block()
                i = len(var) - 1  # The four element set of blocks
                while i > -1:
                    # Something clever
                    val = var[i]  # Iterating through each element of the four element block
                    if val.y == r.y:
                        var.remove(val)  # Adding it to the list if it's "y" value / height is the same var.remove(v)
                        # as the row we want to remove
                    i -= 1  # ".pop(0)" may simulate "queue" functionality
                    # Okay, not using that, but it does turn out you can "pop"
                    # a value, which was essentially, what I was looking ford

        # # pygame.time.delay(1000)
        # [print(de) for de in dele]

