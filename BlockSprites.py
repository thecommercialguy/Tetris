from typing import Tuple, List

from pygame import Rect

from Blocks import Block
import pygame
import random

class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, block, floor_blocks, hit_map):
        super().__init__()
        # block[0 = positions_list][position_list index][0 = x-value]
        # block[0 = positions_list][position_list index][1 = y-value]
        # block[1 = block ID]
        # block[2 = color]
        self.block = block
        #self.rects = []
        self.block_id = block[1][0]
        self.color = block[2]
        self.rot = 0

        # Creating rect objects and rects list initial x-y-positions
        self.rect1 = pygame.Rect(block[0][0][0], block[0][0][1], 34, 34)
        self.rect2 = pygame.Rect(block[0][1][0], block[0][1][1], 34, 34)
        self.rect3 = pygame.Rect(block[0][2][0], block[0][2][1], 34, 34)
        self.rect4 = pygame.Rect(block[0][3][0], block[0][3][1], 34, 34)
        self.rects = [self.rect1, self.rect2, self.rect3, self.rect4]

        # Setting rect objects representing the left wall, right wall, and floor
        self.right_wall = pygame.Rect(592, 32, 2, 684)
        self.left_wall = pygame.Rect(254, 32, 2, 684)
        self.floor = pygame.Rect(254, 712, 340, 2)

        # Initializing current floored blocks
        self.floor_blocks = floor_blocks

        # Initializing current "HitMap"
        self.hit_map = hit_map

    # Allows movement of BlockSprite rects to the right by one unit
    def move_left(self):
        blocks = self.rects
        hit = self.handle_wall_collide(self.left_wall, blocks)

        if not hit:
            for rect_ in self.rects:
                rect_.x -= 34

    # Allows movement of BlockSprite rects to the right by one unit
    def move_right(self):
        blocks = self.rects
        hit = self.handle_wall_collide(self.right_wall, blocks)

        if not hit:
            for rect_ in self.rects:
                rect_.x += 34


    # Returns a boolean value determining if a rect object associated with a "block"
    # has hit a wall or not
    def handle_wall_collide(self, wall, blocks):
        for i, rect in enumerate(blocks):
            hit = blocks[i].colliderect(wall)
            if hit:
                return hit
        return False

    # Method controlling the descent of the rect objects in the "rects" list
    # Returns True if no collision occurs (block can fall)
    # Returns False if collision occurs (block cannot fall)
    def block_descent(self) -> bool:
        if len(self.rects) != 0:
            hit = self.rects[0].colliderect(self.floor)
            hit2 = self.rects[2].colliderect(self.floor)
            hit1 = self.rects[3].colliderect(self.floor)
            hit3 = self.rects[1].colliderect(self.floor)
            if not hit1 and not hit and not hit2 and not hit3:
                # print(hit, hit3, hit2, hit1)
                for rect in self.rects:
                    # rect.y += 34/68
                    rect.y += 34
                return True
        return False

    # Block descent method that checks for collisions with blocks added to the floor
    # Returns False if collision occurs (block cannot fall)
    # Returns True if no collision occurs (block can fall)
    def block_fall_collision_check(self, floors):
        if len(floors) > 0:
            for r in self.rects:
                # To simulate colliding with where the rect would be to register a collision
                temp_rect = pygame.rect.Rect(r.x, r.y+34, r.width, r.height)
                for _floor in floors:
                    collision_index = temp_rect.collidelist(_floor.get_floor_block())
                    if collision_index != -1:
                        return False

        return True

    # Controls block decent by a single unit (+34)
    def block_decent_by_unit(self):
        collision_check = self.hit_map.collide_check(self.rects)
        if collision_check is not None:
            self.rects = collision_check
        else:
            return

    # Obtains a list of rects that are positioned one unit above the highest y-value of the floor block or floor
    # directly beneath it
    def snap_to_floor_(self):
        self.rects = self.hit_map.find_hit(self.rects)

    # Finds the distance between the floor and a BlockSprite's "lowest" y-value
    def snap_operation(self, lowest_y):
        #return self.floor.y - 100 - lowest_y
        return self.floor.y - lowest_y

    # Returns a list of rects representing an outline of the current falling block
    # along the floor or nearest floor block directly beneath it
    def floor_outline(self) -> list[Rect]:
        outline_blocks = []
        for rect in self.rects:
            outline_blocks.append(pygame.rect.Rect(rect.x, rect.y, 34, 34))

        outline = self.hit_map.find_floor(outline_blocks)
        return outline

    # Handles snapping to floor when no blocks have been added to the floor
    def snap_to_floor(self):
        arr = [0,1,2,3]
        diff: int

        print("?????",self.rot)

        if self.block_id == 0:
            if self.rot == 0:
                diff = self.snap_operation(self.rects[3].y)
            elif self.rot == 1:
                diff = self.snap_operation(self.rects[3].y)
                print(diff)
            elif self.rot == 2:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 3:
                diff = self.snap_operation(self.rects[0].y)

        elif self.block_id == 1:
            if self.rot == 0:
                diff = self.snap_operation(self.rects[3].y)
            elif self.rot == 1:
                diff = self.snap_operation(self.rects[1].y)
            elif self.rot == 2:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 3:
                diff = self.snap_operation(self.rects[3].y)
        elif self.block_id == 2:
            diff = self.snap_operation(self.rects[2].y)
        elif self.block_id == 3:
            if self.rot == 0:
                diff = self.snap_operation(self.rects[2].y)
            elif self.rot == 1:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 2:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 3:
                diff = self.snap_operation(self.rects[3].y)

        elif self.block_id == 4:
            if self.rot == 0:
                diff = self.snap_operation(self.rects[1].y)
            elif self.rot == 1:
                diff = self.snap_operation(self.rects[3].y)
            elif self.rot == 2:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 3:
                diff = self.snap_operation(self.rects[1].y)

        elif self.block_id == 5:
            if self.rot == 0:
                diff = self.snap_operation(self.rects[2].y)
            elif self.rot == 1:
                diff = self.snap_operation(self.rects[3].y)
            elif self.rot == 2:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 3:
                diff = self.snap_operation(self.rects[0].y)

        elif self.block_id == 6:
            if self.rot == 0:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 1:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 2:
                diff = self.snap_operation(self.rects[0].y)
            elif self.rot == 3:
                diff = self.snap_operation(self.rects[3].y)


        drop_units = diff / 34

        for rec in self.rects:
            i = 1
            while i < drop_units:
                rec.y += 34
                i += 1


        return True  # Meaning it executed

    # Determines if movement by one unit left or right would result in a collision
    def left_right_collide(self, shift, floored_blocks) -> bool:
        for rect in self.rects:
            temp_rect_x = rect.x + shift
            temp_rect = pygame.rect.Rect(temp_rect_x, rect.y, 34, 34)
            for block in floored_blocks:
                if temp_rect.collidelist(block.get_floor_block()) != -1:
                    return True  # Translation results in a collision

        return False  # Translation does not result in a collision

    # Disables rotation if it collides with a floor block
    def rotation_collide(self, temp_block):
        for temp in temp_block:
            for block in self.floor_blocks:
                if temp.collidelist(block.get_floor_block()) != -1:
                    return True  # Rotation would result in a collision

        return False  # No collision would result from rotation

    # Checks if a block meets conditions for a rotation
    # Returns True if rotation results in a collision
    # Returns False if rotation occurs uninhibited
    def rotate_collision_check(self, block, rotation_step, shape) -> bool:
        left_collision = False
        right_collision = False

        if shape == 0:
            left_rotation_steps = {1: 34, 3: 0}
            right_rotation_steps = {1: 0, 3: 34}

            for rect in block:
                left_collision = rect.colliderect(self.left_wall)
                right_collision = rect.colliderect(self.right_wall)
                if left_collision:
                    break
                if right_collision:
                    break

            if left_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x += left_rotation_steps[rotation_step]
                return True

            if right_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x -= right_rotation_steps[rotation_step]
                return True

        if shape == 1:
            left_rotation_steps = {1: 34, 3: 0}
            right_rotation_steps = {1: 0, 3: 34}

            for rect in block:
                left_collision = rect.colliderect(self.left_wall)
                right_collision = rect.colliderect(self.right_wall)
                if left_collision:
                    break
                if right_collision:
                    break

            if left_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x += left_rotation_steps[rotation_step]
                return True

            if right_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x -= right_rotation_steps[rotation_step]
                return True

        if shape == 3:
            left_rotation_steps = {1: 0, 3: 34}
            right_rotation_steps = {1: 34, 3: 0}
            for rect in block:
                left_collision = rect.colliderect(self.left_wall)
                right_collision = rect.colliderect(self.right_wall)
                if left_collision:
                    break
                if right_collision:
                    break
            if left_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x += 34
                return True
            if right_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x -= 34
                return True

        if shape == 4:
            left_rotation_steps = {1: 34, 3: 0}
            right_rotation_steps = {1: 0, 3: 34}
            for rect in block:
                left_collision = rect.colliderect(self.left_wall)
                right_collision = rect.colliderect(self.right_wall)
                if left_collision:
                    break
                if right_collision:
                    break
            if left_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x += left_rotation_steps[rotation_step]
                return True
            if right_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x -= right_rotation_steps[rotation_step]
                return True

        if shape == 5:
            left_rotation_steps = {1: 0, 3: 34}
            right_rotation_steps = {1: 34, 3: 0}
            for rect in block:
                left_collision = rect.colliderect(self.left_wall)
                right_collision = rect.colliderect(self.right_wall)
                if left_collision:
                    break
                if right_collision:
                    break
            if left_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x += left_rotation_steps[rotation_step]
                return True
            if right_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x -= right_rotation_steps[rotation_step]
                return True

        if shape == 6:
            left_rotation_steps = {1: 68, 3: 34}
            right_rotation_steps = {1: 34, 3: 68}
            for rect in block:
                left_collision = rect.colliderect(self.left_wall)
                right_collision = rect.colliderect(self.right_wall)
                if left_collision:
                    break
                if right_collision:
                    break
            if left_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x += left_rotation_steps[rotation_step]
                return True
            if right_collision:
                for i, rect in enumerate(block):
                    self.rects[i] = rect
                    self.rects[i].x -= right_rotation_steps[rotation_step]
                return True

        return False



    # Handles rotation logic for a BlockSprite
    # Returns True if rotation occurs
    # Returns False if rotation cannot occur
    def rotate(self, i: int):
        self.rot += 1
        if self.rot > 3:
            self.rot = 0
        match self.block_id:
            # Rotations for L shape
            case 0:
                if i == 0:
                    temp_rect1_x = self.rects[0].x + 68
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, self.rects[0].y, 34, 34)
                    temp_rect2_x = self.rects[1].x + 34
                    temp_rect2_y = self.rects[1].y - 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x - 34
                    temp_rect4_y = self.rects[3].y + 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_0 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_0):
                        self.rects[0].x += 68
                        self.rects[1].x += 34
                        self.rects[1].y -= 34
                        self.rects[3].x -= 34
                        self.rects[3].y += 34

                        return True  # Meaning a rotation has occurred
                    return False  # Meaning a rotation has not occurred

                elif i == 1:
                    shape = self.block_id
                    temp_rect1_y = self.rects[0].y + 68
                    temp_rect1 = pygame.rect.Rect(self.rects[0].x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x + 34
                    temp_rect2_y = self.rects[1].y + 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x - 34
                    temp_rect4_y = self.rects[3].y - 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_1 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_1):
                        if not self.rotate_collision_check(temp_rect_1, i, shape):
                            self.rects[0].y += 68
                            self.rects[1].x += 34
                            self.rects[1].y += 34
                            self.rects[3].x -= 34
                            self.rects[3].y -= 34

                        return True
                    return False

                elif i == 2:
                    temp_rect1_x = self.rects[0].x - 68
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, self.rects[0].y, 34, 34)
                    temp_rect2_x = self.rects[1].x - 34
                    temp_rect2_y = self.rects[1].y + 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x + 34
                    temp_rect4_y = self.rects[3].y - 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_2 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_2):
                        self.rects[0].x -= 68
                        self.rects[1].x -= 34
                        self.rects[1].y += 34
                        self.rects[3].x += 34
                        self.rects[3].y -= 34

                        return True
                    return False

                elif i == 3:
                    shape = self.block_id
                    temp_rect1_y = self.rects[0].y - 68
                    temp_rect1 = pygame.rect.Rect(self.rects[0].x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x - 34
                    temp_rect2_y = self.rects[1].y - 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x + 34
                    temp_rect4_y = self.rects[3].y + 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_3 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_3):
                        if not self.rotate_collision_check(temp_rect_3, i, shape):
                            self.rects[0].y -= 68
                            self.rects[1].x -= 34
                            self.rects[1].y -= 34
                            self.rects[3].x += 34
                            self.rects[3].y += 34

                        return True
                    return False
            # Rotations for L* shape
            case 1:
                if i == 0:
                    temp_rect1_y = self.rects[0].y + 68
                    temp_rect1 = pygame.rect.Rect(self.rects[0].x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x - 34
                    temp_rect2_y = self.rects[1].y + 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x + 34
                    temp_rect4_y = self.rects[3].y - 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_0 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_0):
                        self.rects[0].y += 68
                        self.rects[1].x -= 34
                        self.rects[1].y += 34
                        self.rects[3].x += 34
                        self.rects[3].y -= 34

                        return True
                    return False

                elif i == 1:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x - 68
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, self.rects[0].y, 34, 34)
                    temp_rect2_x = self.rects[1].x - 34
                    temp_rect2_y = self.rects[1].y - 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x + 34
                    temp_rect4_y = self.rects[3].y + 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_1 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_1):
                        if not self.rotate_collision_check(temp_rect_1, i, shape):
                            self.rects[0].x -= 68
                            self.rects[1].x -= 34
                            self.rects[1].y -= 34
                            self.rects[3].x += 34
                            self.rects[3].y += 34

                        return True
                    return False

                elif i == 2:
                    temp_rect1_y = self.rects[0].y - 68
                    temp_rect1 = pygame.rect.Rect(self.rects[0].x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x + 34
                    temp_rect2_y = self.rects[1].y - 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x - 34
                    temp_rect4_y = self.rects[3].y + 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_2 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_2):
                        self.rects[0].y -= 68
                        self.rects[1].x += 34
                        self.rects[1].y -= 34
                        self.rects[3].x -= 34
                        self.rects[3].y += 34

                        return True
                    return False

                elif i == 3:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x + 68
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, self.rects[0].y, 34, 34)
                    temp_rect2_x = self.rects[1].x + 34
                    temp_rect2_y = self.rects[1].y + 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x - 34
                    temp_rect4_y = self.rects[3].y - 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_3 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_3):
                        if not self.rotate_collision_check(temp_rect_3, i, shape):
                            self.rects[0].x += 68
                            self.rects[1].x += 34
                            self.rects[1].y += 34
                            self.rects[3].x -= 34
                            self.rects[3].y -= 34

                        return True
                    return False

            # Rotations for S shape
            case 3:
                if i == 0:
                    temp_rect1_x = self.rects[0].x - 34
                    temp_rect1_y = self.rects[0].y + 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x - 34
                    temp_rect3_y = self.rects[2].y - 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_y = self.rects[3].y - 68
                    temp_rect4 = pygame.rect.Rect(self.rects[3].x, temp_rect4_y, 34, 34)
                    temp_rect_0 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_0):
                        self.rects[0].x -= 34
                        self.rects[0].y += 34
                        self.rects[2].x -= 34
                        self.rects[2].y -= 34
                        self.rects[3].y -= 68

                        return True
                    return False

                elif i == 1:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x - 34
                    temp_rect1_y = self.rects[0].y - 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x + 34
                    temp_rect3_y = self.rects[2].y - 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_x = self.rects[3].x + 68
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, self.rects[3].y, 34, 34)
                    temp_rect_1 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_1):
                        if not self.rotate_collision_check(temp_rect_1, i, shape):
                            self.rects[0].x -= 34
                            self.rects[0].y -= 34
                            self.rects[2].x += 34
                            self.rects[2].y -= 34
                            self.rects[3].x += 68

                        return True
                    return False

                elif i == 2:
                    temp_rect1_x = self.rects[0].x + 34
                    temp_rect1_y = self.rects[0].y - 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x + 34
                    temp_rect3_y = self.rects[2].y + 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_y = self.rects[3].y + 68
                    temp_rect4 = pygame.rect.Rect(self.rects[3].x, temp_rect4_y, 34, 34)
                    temp_rect_2 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_2):
                        self.rects[0].x += 34
                        self.rects[0].y -= 34
                        self.rects[2].x += 34
                        self.rects[2].y += 34
                        # creating a "diagonal"
                        self.rects[3].y += 68

                        return True
                    return False

                elif i == 3:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x + 34
                    temp_rect1_y = self.rects[0].y + 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x - 34
                    temp_rect3_y = self.rects[2].y + 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_x = self.rects[3].x - 68
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, self.rects[3].y, 34, 34)
                    temp_rect_3 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_3):
                        if not self.rotate_collision_check(temp_rect_3, i, shape):
                            self.rects[0].x += 34
                            self.rects[0].y += 34
                            self.rects[2].x -= 34
                            self.rects[2].y += 34
                            self.rects[3].x -= 68


                        return True
                    return False

            # Rotations for T* shape
            case 4:
                if i == 0:
                    temp_rect1_x = self.rects[0].x + 34
                    temp_rect1_y = self.rects[0].y + 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x + 34
                    temp_rect2_y = self.rects[1].y - 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x - 34
                    temp_rect4_y = self.rects[3].y + 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_0 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_0):
                        self.rects[0].x += 34
                        self.rects[0].y += 34
                        self.rects[1].x += 34
                        self.rects[1].y -= 34
                        self.rects[3].x -= 34
                        self.rects[3].y += 34

                        return True
                    return False

                elif i == 1:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x - 34
                    temp_rect1_y = self.rects[0].y + 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x + 34
                    temp_rect2_y = self.rects[1].y + 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x - 34
                    temp_rect4_y = self.rects[3].y - 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_1 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_1):
                        if not self.rotate_collision_check(temp_rect_1, i, shape):
                            self.rects[0].x -= 34
                            self.rects[0].y += 34
                            self.rects[1].x += 34
                            self.rects[1].y += 34
                            self.rects[3].x -= 34
                            self.rects[3].y -= 34

                        return True
                    return False

                elif i == 2:
                    temp_rect1_x = self.rects[0].x - 34
                    temp_rect1_y = self.rects[0].y - 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x - 34
                    temp_rect2_y = self.rects[1].y + 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x + 34
                    temp_rect4_y = self.rects[3].y - 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_2 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_2):
                        self.rects[0].x -= 34
                        self.rects[0].y -= 34
                        self.rects[1].x -= 34
                        self.rects[1].y += 34
                        self.rects[3].x += 34
                        self.rects[3].y -= 34

                        return True
                    return False

                elif i == 3:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x + 34
                    temp_rect1_y = self.rects[0].y - 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x - 34
                    temp_rect2_y = self.rects[1].y - 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x + 34
                    temp_rect4_y = self.rects[3].y + 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_3 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_3):
                        if not self.rotate_collision_check(temp_rect_3, i, shape):
                            self.rects[0].x += 34
                            self.rects[0].y -= 34
                            self.rects[1].x -= 34
                            self.rects[1].y -= 34
                            self.rects[3].x += 34
                            self.rects[3].y += 34

                        return True
                    return False

            # Rotations for S* shape
            case 5:
                if i == 0:
                    temp_rect1_x = self.rects[0].x + 34
                    temp_rect1_y = self.rects[0].y - 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x - 34
                    temp_rect3_y = self.rects[2].y - 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_x = self.rects[3].x - 68
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, self.rects[3].y, 34, 34)
                    temp_rect_0 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_0):
                        self.rects[0].x += 34
                        self.rects[0].y -= 34
                        self.rects[2].x -= 34
                        self.rects[2].y -= 34
                        self.rects[3].x -= 68

                        return True
                    return False

                elif i == 1:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x + 34
                    temp_rect1_y = self.rects[0].y + 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x + 34
                    temp_rect3_y = self.rects[2].y - 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_y = self.rects[3].y - 68
                    temp_rect4 = pygame.rect.Rect(self.rects[3].x, temp_rect4_y, 34, 34)
                    temp_rect_1 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_1):
                        if not self.rotate_collision_check(temp_rect_1, i, shape):
                            self.rects[0].x += 34
                            self.rects[0].y += 34
                            self.rects[2].x += 34
                            self.rects[2].y -= 34
                            self.rects[3].y -= 68

                        return True
                    return False

                elif i == 2:
                    temp_rect1_x = self.rects[0].x - 34
                    temp_rect1_y = self.rects[0].y + 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x + 34
                    temp_rect3_y = self.rects[2].y + 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_x = self.rects[3].x + 68
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, self.rects[3].y, 34, 34)
                    temp_rect_2 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_2):
                        self.rects[0].x -= 34
                        self.rects[0].y += 34
                        self.rects[2].x += 34
                        self.rects[2].y += 34
                        # creating a "diagonal"
                        self.rects[3].x += 68

                        return True
                    return False

                elif i == 3:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x - 34
                    temp_rect1_y = self.rects[0].y - 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x - 34
                    temp_rect3_y = self.rects[2].y + 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_y = self.rects[3].y + 68
                    temp_rect4 = pygame.rect.Rect(self.rects[3].x, temp_rect4_y, 34, 34)
                    temp_rect_3 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_3):
                        if not self.rotate_collision_check(temp_rect_3, i, shape):
                            self.rects[0].x -= 34
                            self.rects[0].y -= 34
                            self.rects[2].x -= 34
                            self.rects[2].y += 34
                            self.rects[3].y += 68

                        return True
                    return False

            # Rotations for ---- shape
            case 6:
                if i == 0:
                    temp_rect1_x = self.rects[0].x + 68
                    temp_rect1_y = self.rects[0].y + 68
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x + 34
                    temp_rect2_y = self.rects[1].y + 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x - 34
                    temp_rect4_y = self.rects[3].y - 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_0 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_0):
                        self.rects[0].x += 68
                        self.rects[0].y += 68
                        self.rects[1].x += 34
                        self.rects[1].y += 34
                        self.rects[3].x -= 34
                        self.rects[3].y -= 34

                        return True
                    return False

                elif i == 1:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x + 34
                    temp_rect1_y = self.rects[0].y - 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x - 34
                    temp_rect3_y = self.rects[2].y + 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_x = self.rects[3].x - 68
                    temp_rect4_y = self.rects[3].y + 68
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_1 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_1):
                        if not self.rotate_collision_check(temp_rect_1, i, shape):
                            self.rects[0].x += 34
                            self.rects[0].y -= 34
                            self.rects[2].x -= 34
                            self.rects[2].y += 34
                            self.rects[3].x -= 68
                            self.rects[3].y += 68

                        return True
                    return False

                elif i == 2:
                    temp_rect1_x = self.rects[0].x - 68
                    temp_rect1_y = self.rects[0].y - 68
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2_x = self.rects[1].x - 34
                    temp_rect2_y = self.rects[1].y - 34
                    temp_rect2 = pygame.rect.Rect(temp_rect2_x, temp_rect2_y, 34, 34)
                    temp_rect3 = self.rects[2]
                    temp_rect4_x = self.rects[3].x + 34
                    temp_rect4_y = self.rects[3].y + 34
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_2 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_2):
                        self.rects[0].x -= 68
                        self.rects[0].y -= 68
                        self.rects[1].x -= 34
                        self.rects[1].y -= 34
                        self.rects[3].x += 34
                        self.rects[3].y += 34

                        return True
                    return False

                elif i == 3:
                    shape = self.block_id
                    temp_rect1_x = self.rects[0].x - 34
                    temp_rect1_y = self.rects[0].y + 34
                    temp_rect1 = pygame.rect.Rect(temp_rect1_x, temp_rect1_y, 34, 34)
                    temp_rect2 = self.rects[1]
                    temp_rect3_x = self.rects[2].x + 34
                    temp_rect3_y = self.rects[2].y - 34
                    temp_rect3 = pygame.rect.Rect(temp_rect3_x, temp_rect3_y, 34, 34)
                    temp_rect4_x = self.rects[3].x + 68
                    temp_rect4_y = self.rects[3].y - 68
                    temp_rect4 = pygame.rect.Rect(temp_rect4_x, temp_rect4_y, 34, 34)
                    temp_rect_3 = [temp_rect1, temp_rect2, temp_rect3, temp_rect4]
                    if not self.rotation_collide(temp_rect_3):
                        if not self.rotate_collision_check(temp_rect_3, i, shape):
                            self.rects[0].x -= 34
                            self.rects[0].y += 34
                            self.rects[2].x += 34
                            self.rects[2].y -= 34
                            self.rects[3].x += 68
                            self.rects[3].y -= 68

                        return True
                    return False

    # Returns the block's color
    def get_color(self):
        return self.color

    # Deletes all rect objects form rects list
    def delete_blocks(self) -> bool:
        self.rects.clear()
        if len(self.rects) == 0:
            return True
        return False

