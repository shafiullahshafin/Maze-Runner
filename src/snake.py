import pygame
from src.constants import *

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 3
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (0, 0) # Stationary at start
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_x = cur[0] + (x * GRID_SIZE)
        new_y = cur[1] + (y * GRID_SIZE)

        # Wall wrap-around (Nokia style)
        if new_x < 0:
            new_x = SCREEN_WIDTH - GRID_SIZE
        elif new_x >= SCREEN_WIDTH:
            new_x = 0
        
        if new_y < 0:
            new_y = SCREEN_HEIGHT - GRID_SIZE
        elif new_y >= SCREEN_HEIGHT:
            new_y = 0
            
        new = (new_x, new_y)

        if len(self.positions) > 2 and new in self.positions[2:]:
            return False # Hit self

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return True

    def reset_position(self):
        self.length = 3
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (0, 0)

    def draw(self, surface):
        for index, p in enumerate(self.positions):
            # Draw rounded segments (circles)
            center = (p[0] + GRID_SIZE // 2, p[1] + GRID_SIZE // 2)
            radius = GRID_SIZE // 2
            
            # Head color slightly different or same
            color = self.color
            if index == 0:
                color = (40, 180, 100) # Slightly darker green for head
            
            pygame.draw.circle(surface, color, center, radius)
            
            # Draw eyes if it's the head
            if index == 0:
                eye_radius = 3
                eye_offset_x = radius // 2
                eye_offset_y = radius // 2
                
                # Determine eye positions based on direction
                dx, dy = self.direction
                
                # Default to looking right if stationary
                if dx == 0 and dy == 0:
                    dx = 1
                
                # Calculate eye centers
                # If moving right (1, 0): eyes at (center_x + off, center_y +/- off)
                # If moving left (-1, 0): eyes at (center_x - off, center_y +/- off)
                # If moving up (0, -1): eyes at (center_x +/- off, center_y - off)
                # If moving down (0, 1): eyes at (center_x +/- off, center_y + off)
                
                eye1 = (0, 0)
                eye2 = (0, 0)
                
                if dx != 0: # Horizontal
                    eye1 = (center[0] + (dx * eye_offset_x), center[1] - eye_offset_y)
                    eye2 = (center[0] + (dx * eye_offset_x), center[1] + eye_offset_y)
                else: # Vertical
                    eye1 = (center[0] - eye_offset_x, center[1] + (dy * eye_offset_y))
                    eye2 = (center[0] + eye_offset_x, center[1] + (dy * eye_offset_y))
                    
                pygame.draw.circle(surface, BLACK, eye1, eye_radius)
                pygame.draw.circle(surface, BLACK, eye2, eye_radius)

    def grow(self):
        self.length += 1
        self.score += 10
