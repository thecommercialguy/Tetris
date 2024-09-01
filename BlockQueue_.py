from typing import Tuple, List

from pygame import Rect

from Blocks import Block
from BlockSprites import BlockSprite
from FloorSprites import FloorSprite
from BoardSprites import BoardSprite
from ScoreBoard_ import ScoreBoard
from HitMap_ import HitMap
import pygame
import random




class BlockQueue:
    # Initializes block queue
    def __init__(self, blocks: Block, block_dict, screen: pygame.Surface):
        # Holds dictionary for miniaturized blocks
        self.blocks = blocks.get_blocks_data_conv()
        self.width = 16
        self.colors: List[Tuple[int, int, int]] = []
        self.shapes: List[int] = []
        self.block_queue = []
        # Contains "shades" associated with each shape's primary color
        self.block_dict = block_dict
        self.screen = screen

    # Pushes a new block into the queue
    def push_queue_block(self):
        block = self.blocks
        index = random.randint(0, 6)
        self.shapes.append(index)

        new_block = block[index]

        positions = new_block[0]
        self.colors.append(new_block[2])
        queue_block = []
        for i in range(len(positions)):
            x_pos = positions[i][0]
            y_pos = positions[i][1]

            queue_rect = pygame.rect.Rect(x_pos, y_pos, 16, 16)

            queue_block.append(queue_rect)

        self.block_queue.append(queue_block)




    # Sets up initial queue blocks
    def set_queue_blocks(self):
        block = self.blocks
        random_index_0 = random.randint(0, 6)
        random_index_1 = random.randint(0, 6)
        random_index_2 = random.randint(0, 6)

        self.shapes = [random_index_0, random_index_1, random_index_2]

        block0_r = block[random_index_0]
        block1_r = block[random_index_1]
        block2_r = block[random_index_2]

        to_arrange = [block0_r, block1_r, block2_r]

        # Populates the queue
        for block in to_arrange:
            # Accesses list containing block's x-, y-positions
            positions = block[0]
            # Retrieves the block's color
            self.colors.append(block[2])
            queue_block = []

            for i in range(len(positions)):
                # accessing array
                x_pos = positions[i][0]
                y_pos = positions[i][1]

                queue_rect = pygame.rect.Rect(x_pos, y_pos, 16, 16)

                queue_block.append(queue_rect)

            self.block_queue.append(queue_block)

    # Removing leading color, block, and shape
    def dequeue_block(self) -> int:
        self.colors.pop(0)
        self.block_queue.pop(0)
        return self.shapes.pop(0)

    # Draws the block queue
    def draw_queue_blocks(self):
        screen = self.screen
        shifts = [0, 68, 136]
        for i, q_block in enumerate(self.block_queue):
            for q_rect in q_block:
                x_aug = q_rect.x + shifts[i]
                pygame.draw.rect(screen, self.colors[i], (x_aug, q_rect.y, 16, 16), 0, 3)
                pygame.draw.rect(screen, self.block_dict[self.colors[i]][0],
                                 (x_aug + 0.94118, q_rect.y + 1.8824, 1, 12.235), 1, 8)
                pygame.draw.rect(screen, self.block_dict[self.colors[i]][1],
                                 (x_aug+ 1.8824, q_rect.y + 14.118, 12.235, 0.94118), 1, 8)
                pygame.draw.rect(screen, "white", (x_aug+14.118, q_rect.y+1.8824, 1, 12.235), 0, 25)
                pygame.draw.rect(screen, "black", (x_aug, q_rect.y, 16, 16), 1, 3)
