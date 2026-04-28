import pygame
from collections import deque


def draw_pencil(surface, color, start_pos, end_pos, size):
    pygame.draw.line(surface, color, start_pos, end_pos, size)


def draw_line(surface, color, start_pos, end_pos, size):
    pygame.draw.line(surface, color, start_pos, end_pos, size)


def draw_rect(surface, color, start_pos, end_pos, size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    pygame.draw.rect(surface, color, rect, size)


def draw_circle(surface, color, start_pos, end_pos, size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    pygame.draw.circle(surface, color, start_pos, radius, size)


def flood_fill(surface, x, y, fill_color):
    width, height = surface.get_size()

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))