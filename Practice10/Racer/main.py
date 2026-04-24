import pygame
import random
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800,600))
running = True
clock = pygame.time.Clock()

# Car
car = pygame.image.load("Practice10/Racer/images/car.png").convert_alpha()
car = pygame.transform.scale(car, (120,150))
car_x = 335
car_y = 400
car_speed = 2

# Background
bg = pygame.image.load("Practice10/Racer/images/background.png").convert_alpha()
bg = pygame.transform.scale(bg, screen.get_size())
bg_sound = pygame.mixer.Sound("Practice10/Racer/music,sounds/bg_sound.mp3")
bg_sound.play()
bg_y = 0

# Enemy
enemy = pygame.image.load("Practice10/Racer/images/enemy1.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (170,170))
enemy_list_in_game = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 500)

car_mask = pygame.mask.from_surface(car)
enemy_mask = pygame.mask.from_surface(enemy)

gameplay = True

label = pygame.font.Font(None, 40)
lose_label = label.render("You lose!", True, (255,0,0))
restart_label = label.render("Restart", True, (255,255,255))
restart_label_rect = restart_label.get_rect(topleft=(340,300))


while running:

    if gameplay:
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - 600))
        screen.blit(car, (car_x, car_y))

        car_rect = car.get_rect(topleft=(car_x, car_y))

        if enemy_list_in_game:
            for el in enemy_list_in_game:
                screen.blit(enemy, el)
                el.y += 2

                offset = (el.x - car_x, el.y - car_y)
                if car_mask.overlap(enemy_mask, offset):
                    gameplay = False

        enemy_list_in_game = [el for el in enemy_list_in_game if el.y < 600]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 150:
            car_x -= car_speed
        elif keys[pygame.K_RIGHT] and car_x < 525:
            car_x += car_speed
        elif keys[pygame.K_UP] and car_y > 50:
            car_y -= car_speed
        elif keys[pygame.K_DOWN] and car_y < 450:
            car_y += car_speed

        bg_y += 2
        if bg_y >= 600:
            bg_y = 0

    else:
        screen.fill("BLACK")
        screen.blit(lose_label,(330,200))
        screen.blit(restart_label,(restart_label_rect))
        bg_sound.stop()
        
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            car_x = 335
            car_y = 400
            enemy_list_in_game.clear()
            bg_sound.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if gameplay and event.type == enemy_timer:
            new_x = random.randint(150, 525)
            enemy_list_in_game.append(enemy.get_rect(topleft=(new_x, -150)))

    pygame.display.update()
    clock.tick(220)

pygame.quit()