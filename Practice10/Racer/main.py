import pygame
import random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Racer Game")

running = True
clock = pygame.time.Clock()

# Car
car = pygame.image.load("Practice10/Racer/images/car.png").convert_alpha()
car = pygame.transform.scale(car, (120, 150))
car_x = 335
car_y = 400
car_speed = 4

# Background
bg = pygame.image.load("Practice10/Racer/images/background.png").convert_alpha()
bg = pygame.transform.scale(bg, screen.get_size())

bg_sound = pygame.mixer.Sound("Practice10/Racer/music,sounds/bg_sound.mp3")
bg_sound.play(-1)

bg_y = 0

# Enemy
enemy = pygame.image.load("Practice10/Racer/images/enemy1.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (170, 170))

enemy_list_in_game = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

# Coin
coin_img = pygame.image.load("Practice10/Racer/images/coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (45, 45))

coin_list = []
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, 1200)

# Score
score = 0

# Masks
car_mask = pygame.mask.from_surface(car)
enemy_mask = pygame.mask.from_surface(enemy)

gameplay = True

# Text
label = pygame.font.Font(None, 40)

lose_label = label.render("You lose!", True, (255, 0, 0))
restart_label = label.render("Restart", True, (255, 255, 255))
restart_label_rect = restart_label.get_rect(topleft=(340, 300))


while running:

    if gameplay:
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - 600))

        screen.blit(car, (car_x, car_y))
        car_rect = car.get_rect(topleft=(car_x, car_y))

        # Enemies
        for el in enemy_list_in_game:
            screen.blit(enemy, el)
            el.y += 3

            offset = (el.x - car_x, el.y - car_y)

            if car_mask.overlap(enemy_mask, offset):
                gameplay = False

        enemy_list_in_game = [el for el in enemy_list_in_game if el.y < 600]

        # Coins
        for coin in coin_list[:]:
            screen.blit(coin_img, coin)
            coin.y += 4

            if car_rect.colliderect(coin):
                score += 1
                coin_list.remove(coin)

        coin_list = [coin for coin in coin_list if coin.y < 600]

        # Score text
        score_text = label.render(f"Coins: {score}", True, (255, 255, 0))
        screen.blit(score_text, (20, 20))

        # Car movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and car_x > 150:
            car_x -= car_speed
        elif keys[pygame.K_RIGHT] and car_x < 525:
            car_x += car_speed
        elif keys[pygame.K_UP] and car_y > 50:
            car_y -= car_speed
        elif keys[pygame.K_DOWN] and car_y < 450:
            car_y += car_speed

        # Background movement
        bg_y += 3

        if bg_y >= 600:
            bg_y = 0

    else:
        screen.fill("BLACK")

        screen.blit(lose_label, (330, 200))

        final_score = label.render(f"Your coins: {score}", True, (255, 255, 0))
        screen.blit(final_score, (300, 250))

        screen.blit(restart_label, restart_label_rect)

        bg_sound.stop()

        mouse = pygame.mouse.get_pos()

        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            car_x = 335
            car_y = 400
            enemy_list_in_game.clear()
            coin_list.clear()
            score = 0
            bg_sound.play(-1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if gameplay and event.type == enemy_timer:
            new_x = random.randint(150, 525)
            enemy_list_in_game.append(enemy.get_rect(topleft=(new_x, -150)))

        if gameplay and event.type == coin_timer:
            coin_x = random.randint(150, 525)
            coin_list.append(coin_img.get_rect(topleft=(coin_x, -50)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()