import pygame
import random
import time
import os
from persistence import add_score

BASE = os.path.dirname(__file__)

WIDTH = 800
HEIGHT = 600

ROAD_X = 180
ROAD_W = 440
LANES = [235, 345, 455, 565]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (30, 170, 60)
BLUE = (40, 100, 255)
YELLOW = (255, 220, 40)
ORANGE = (255, 140, 0)
BROWN = (120, 70, 30)


class RacerGame:
    def __init__(self, screen, username, settings):
        self.screen = screen
        self.username = username
        self.settings = settings

        self.font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load(os.path.join(BASE, "assets", "background.png")).convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.bg_y = 0

        self.car_image = pygame.image.load(os.path.join(BASE, "assets", "car.png")).convert_alpha()
        self.car_image = pygame.transform.scale(self.car_image, (50, 80))

        self.enemy_image = pygame.image.load(os.path.join(BASE, "assets", "enemy.png")).convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (50, 80))

        self.coin_image = pygame.image.load(os.path.join(BASE, "assets", "coins.png")).convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (24, 24))

        self.player = pygame.Rect(370, 470, 50, 80)

        self.traffic = []
        self.obstacles = []
        self.powerups = []
        self.coins = []

        self.distance = 0
        self.finish_distance = 3000
        self.coins_count = 0
        self.score = 0

        self.base_speed = 5
        self.road_speed = 5

        self.active_powerup = None
        self.powerup_end_time = 0
        self.shield = False

        self.running = True
        self.game_over = False

        self.spawn_timer = 0
        self.obstacle_timer = 0
        self.powerup_timer = 0
        self.coin_timer = 0

        self.set_difficulty()

    def set_difficulty(self):
        difficulty = self.settings["difficulty"]

        if difficulty == "easy":
            self.spawn_limit = 70
            self.obstacle_limit = 120
        elif difficulty == "hard":
            self.spawn_limit = 35
            self.obstacle_limit = 70
        else:
            self.spawn_limit = 50
            self.obstacle_limit = 90

    def safe_lane(self):
        possible = []

        for lane in LANES:
            if abs(lane - self.player.centerx) > 80:
                possible.append(lane)

        if not possible:
            possible = LANES

        return random.choice(possible)

    def spawn_traffic(self):
        lane = self.safe_lane()
        car = pygame.Rect(lane - 25, -90, 50, 80)
        self.traffic.append(car)

    def spawn_obstacle(self):
        lane = self.safe_lane()
        kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])
        obstacle = {
            "rect": pygame.Rect(lane - 30, -60, 60, 35),
            "type": kind
        }
        self.obstacles.append(obstacle)

    def spawn_powerup(self):
        lane = self.safe_lane()
        kind = random.choice(["nitro", "shield", "repair"])
        powerup = {
            "rect": pygame.Rect(lane - 18, -40, 36, 36),
            "type": kind,
            "created": time.time()
        }
        self.powerups.append(powerup)

    def spawn_coin(self):
        lane = random.choice(LANES)
        self.coins.append(pygame.Rect(lane - 12, -30, 24, 24))

    def update_difficulty(self):
        extra = int(self.distance // 600)
        self.road_speed = self.base_speed + extra

        if self.active_powerup == "nitro":
            self.road_speed += 4

        self.spawn_limit = max(20, self.spawn_limit - extra)
        self.obstacle_limit = max(40, self.obstacle_limit - extra)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

    def move_player(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.player.left > ROAD_X:
            self.player.x -= 7
        if keys[pygame.K_RIGHT] and self.player.right < ROAD_X + ROAD_W:
            self.player.x += 7
        if keys[pygame.K_UP] and self.player.top > 90:
            self.player.y -= 5
        if keys[pygame.K_DOWN] and self.player.bottom < HEIGHT - 20:
            self.player.y += 5

    def update_objects(self):
        for car in self.traffic:
            car.y += self.road_speed + 1

        for obstacle in self.obstacles:
            obstacle["rect"].y += self.road_speed
            if obstacle["type"] == "barrier":
                obstacle["rect"].x += random.choice([-1, 0, 1])

        for powerup in self.powerups:
            powerup["rect"].y += self.road_speed

        for coin in self.coins:
            coin.y += self.road_speed

        self.traffic = [c for c in self.traffic if c.y < HEIGHT + 100]
        self.obstacles = [o for o in self.obstacles if o["rect"].y < HEIGHT + 100]
        self.coins = [c for c in self.coins if c.y < HEIGHT + 50]

        now = time.time()
        self.powerups = [
            p for p in self.powerups
            if p["rect"].y < HEIGHT + 50 and now - p["created"] < 6
        ]

    def check_collisions(self):
        for car in self.traffic[:]:
            if self.player.colliderect(car):
                if self.shield:
                    self.shield = False
                    self.active_powerup = None
                    self.traffic.remove(car)
                else:
                    self.end_game()

        for obstacle in self.obstacles[:]:
            if self.player.colliderect(obstacle["rect"]):
                if self.shield:
                    self.shield = False
                    self.active_powerup = None
                    self.obstacles.remove(obstacle)
                else:
                    if obstacle["type"] == "oil":
                        self.player.x += random.choice([-50, 50])
                    elif obstacle["type"] == "speed_bump":
                        self.road_speed = max(3, self.road_speed - 2)
                    else:
                        self.end_game()

        for coin in self.coins[:]:
            if self.player.colliderect(coin):
                self.coins.remove(coin)
                self.coins_count += 1

        for powerup in self.powerups[:]:
            if self.player.colliderect(powerup["rect"]):
                self.collect_powerup(powerup)
                self.powerups.remove(powerup)

    def collect_powerup(self, powerup):
        if self.active_powerup is not None:
            return

        kind = powerup["type"]

        if kind == "nitro":
            self.active_powerup = "nitro"
            self.powerup_end_time = time.time() + 4

        elif kind == "shield":
            self.active_powerup = "shield"
            self.shield = True

        elif kind == "repair":
            if self.obstacles:
                self.obstacles.pop(0)

    def update_powerup(self):
        if self.active_powerup == "nitro" and time.time() > self.powerup_end_time:
            self.active_powerup = None

    def end_game(self):
        self.game_over = True
        add_score(self.username, self.score, int(self.distance))

    def update_score(self):
        self.distance += self.road_speed * 0.2
        self.score = int(self.distance) + self.coins_count * 10

        if self.distance >= self.finish_distance:
            self.score += 500
            self.end_game()

    def draw_road(self):
        self.bg_y += self.road_speed

        if self.bg_y >= HEIGHT:
            self.bg_y = 0

        self.screen.blit(self.bg, (0, self.bg_y))
        self.screen.blit(self.bg, (0, self.bg_y - HEIGHT))

    def draw_player(self):
        self.screen.blit(self.car_image, self.player)

        if self.shield:
            pygame.draw.circle(self.screen, BLUE, self.player.center, 48, 3)

    def draw_objects(self):
        for car in self.traffic:
            self.screen.blit(self.enemy_image, car)

        for obstacle in self.obstacles:
            rect = obstacle["rect"]
            kind = obstacle["type"]

            if kind == "barrier":
                color = ORANGE
            elif kind == "oil":
                color = BLACK
            elif kind == "pothole":
                color = BROWN
            else:
                color = YELLOW

            pygame.draw.rect(self.screen, color, rect, border_radius=6)

        for coin in self.coins:
            self.screen.blit(self.coin_image, coin)

        for powerup in self.powerups:
            rect = powerup["rect"]
            kind = powerup["type"]

            if kind == "nitro":
                color = ORANGE
                letter = "N"
            elif kind == "shield":
                color = BLUE
                letter = "S"
            else:
                color = GREEN
                letter = "R"

            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            text = self.font.render(letter, True, WHITE)
            self.screen.blit(text, (rect.x + 9, rect.y + 5))

    def draw_hud(self):
        remaining = max(0, int(self.finish_distance - self.distance))

        texts = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Coins: {self.coins_count}",
            f"Distance: {int(self.distance)} m",
            f"Remaining: {remaining} m",
            f"Power-up: {self.active_powerup if self.active_powerup else 'none'}"
        ]

        y = 10
        for text in texts:
            surf = self.font.render(text, True, WHITE)
            self.screen.blit(surf, (10, y))
            y += 28

        if self.active_powerup == "nitro":
            left = max(0, int(self.powerup_end_time - time.time()))
            surf = self.font.render(f"Nitro time: {left}s", True, YELLOW)
            self.screen.blit(surf, (10, y))

    def spawn_logic(self):
        self.spawn_timer += 1
        self.obstacle_timer += 1
        self.powerup_timer += 1
        self.coin_timer += 1

        if self.spawn_timer > self.spawn_limit:
            self.spawn_traffic()
            self.spawn_timer = 0

        if self.obstacle_timer > self.obstacle_limit:
            self.spawn_obstacle()
            self.obstacle_timer = 0

        if self.powerup_timer > 220:
            self.spawn_powerup()
            self.powerup_timer = 0

        if self.coin_timer > 45:
            self.spawn_coin()
            self.coin_timer = 0

    def run(self):
        while self.running:
            result = self.handle_events()

            if result == "quit":
                return "quit"

            if self.game_over:
                return {
                    "score": self.score,
                    "distance": int(self.distance),
                    "coins": self.coins_count
                }

            self.move_player()
            self.update_difficulty()
            self.spawn_logic()
            self.update_objects()
            self.check_collisions()
            self.update_powerup()
            self.update_score()

            self.draw_road()
            self.draw_objects()
            self.draw_player()
            self.draw_hud()

            pygame.display.flip()
            self.clock.tick(60)