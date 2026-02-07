import pygame

def draw_text(surface, text, font, color, center_pos):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=center_pos)
    surface.blit(text_surface, rect)
