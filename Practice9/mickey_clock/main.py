import pygame
import datetime
import os

pygame.init()

screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()

base = os.path.dirname(__file__)

clockpng = pygame.image.load(os.path.join(base, "images", "clock.PNG")).convert_alpha()
minpng = pygame.image.load(os.path.join(base, "images", "righthand.PNG")).convert_alpha()
secpng = pygame.image.load(os.path.join(base, "images", "lefthand.PNG")).convert_alpha()

center = (1280 // 2, 800 // 2)

MIN_OFFSET = 0
SEC_OFFSET = 0

# 🔥 поднимаем сильно вверх
SEC_Y_OFFSET = -15

running = True

while running:
    now = datetime.datetime.now()

    minutes = now.minute
    seconds = now.second

    min_ang = minutes * 6 + seconds * 0.1
    sec_ang = seconds * 6

    min_rot = pygame.transform.rotate(minpng, -(min_ang + MIN_OFFSET))
    sec_rot = pygame.transform.rotate(secpng, -(sec_ang + SEC_OFFSET))

    min_rect = min_rot.get_rect(center=center)
    sec_rect = sec_rot.get_rect(center=(center[0], center[1] + SEC_Y_OFFSET))

    screen.blit(clockpng, (0, 0))
    screen.blit(min_rot, min_rect)
    screen.blit(sec_rot, sec_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()