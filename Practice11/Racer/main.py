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
car_speed = 3

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
pygame.time.set_timer(enemy_timer, 900)

enemy_speed = 3  # скорость врагов

# Coins
coin_img = pygame.image.load("Practice10/Racer/images/coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (40,40))
coin_list = []
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, 1000)

coins_collected = 0  # счетчик монет

car_mask = pygame.mask.from_surface(car)
enemy_mask = pygame.mask.from_surface(enemy)
coin_mask = pygame.mask.from_surface(coin_img)

gameplay = True

label = pygame.font.Font(None, 40)
lose_label = label.render("You lose!", True, (255,0,0))
restart_label = label.render("Restart", True, (255,255,255))
restart_label_rect = restart_label.get_rect(topleft=(340,300))

score_label = pygame.font.Font(None, 30)

while running:

    if gameplay:
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - 600))
        screen.blit(car, (car_x, car_y))

        car_rect = car.get_rect(topleft=(car_x, car_y))

        # --- ENEMIES ---
        if enemy_list_in_game:
            for el in enemy_list_in_game:
                screen.blit(enemy, el)
                el.y += enemy_speed

                offset = (el.x - car_x, el.y - car_y)
                if car_mask.overlap(enemy_mask, offset):
                    gameplay = False

        enemy_list_in_game = [el for el in enemy_list_in_game if el.y < 600]

        # --- COINS ---
        if coin_list:
            for coin in coin_list:
                screen.blit(coin_img, coin["rect"])
                coin["rect"].y += 2

                offset = (coin["rect"].x - car_x, coin["rect"].y - car_y)
                if car_mask.overlap(coin_mask, offset):
                    coins_collected += coin["value"]  # добавляем вес монеты
                    coin_list.remove(coin)

        coin_list = [c for c in coin_list if c["rect"].y < 600]

        # --- SPEED INCREASE ---
        if coins_collected >= 10:
            enemy_speed = 4
        if coins_collected >= 20:
            enemy_speed = 6

        # --- MOVEMENT ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 150:
            car_x -= car_speed
        elif keys[pygame.K_RIGHT] and car_x < 525:
            car_x += car_speed
        elif keys[pygame.K_UP] and car_y > 50:
            car_y -= car_speed
        elif keys[pygame.K_DOWN] and car_y < 450:
            car_y += car_speed

        # --- BACKGROUND ---
        bg_y += 2
        if bg_y >= 600:
            bg_y = 0

        # --- SCORE DISPLAY ---
        score_text = score_label.render(f"Coins: {coins_collected}", True, (255,255,0))
        screen.blit(score_text, (650, 20))

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
            coin_list.clear()
            coins_collected = 0
            enemy_speed = 2
            bg_sound.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- SPAWN ENEMY ---
        if gameplay and event.type == enemy_timer:
            new_x = random.randint(150, 525)
            enemy_list_in_game.append(enemy.get_rect(topleft=(new_x, -150)))

        # --- SPAWN COIN ---
        if gameplay and event.type == coin_timer:
            new_x = random.randint(150, 525)

            # случайный вес монеты
            value = random.choice([1, 2, 3])

            coin_list.append({
                "rect": coin_img.get_rect(topleft=(new_x, -50)),
                "value": value
            })

    pygame.display.update()
    clock.tick(200)

pygame.quit()