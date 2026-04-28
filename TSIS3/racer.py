import pygame  # Импортируем pygame для создания игры, отрисовки объектов и работы с клавишами
import random  # Нужен для случайного выбора полос, машин, монет, препятствий
import math    # Нужен для анимаций через sin(), например пульсация power-up и движение монет


# =========================
# ЦВЕТА
# =========================

PINK = (255, 105, 180)
DEEP_PINK = (220, 20, 120)
WHITE = (255, 255, 255)
BLACK = (10, 5, 15)
DARK = (18, 8, 28)
ROAD_DARK = (30, 18, 42)
ROAD_MID = (40, 25, 55)
LANE_MARK = (255, 210, 80)
GOLD = (255, 220, 80)
RED = (255, 70, 90)
GREEN = (80, 220, 120)
CYAN = (100, 200, 255)
ORANGE = (255, 160, 30)
GRAY = (120, 100, 130)
BLUE = (50, 120, 255)


# Цвета машины игрока, которые можно выбрать в настройках
CAR_COLORS = {
    "pink": (255, 105, 180),
    "mint": (100, 230, 160),
    "lavender": (180, 140, 255),
    "white": (240, 240, 250),
    "red": (255, 80, 80),
}


# Настройки сложности
# base_speed — базовая скорость
# traffic_freq — частота появления машин
# obstacle_freq — частота появления препятствий
DIFF_SETTINGS = {
    "easy": {"base_speed": 4, "traffic_freq": 180, "obstacle_freq": 220},
    "normal": {"base_speed": 6, "traffic_freq": 120, "obstacle_freq": 160},
    "hard": {"base_speed": 9, "traffic_freq": 80, "obstacle_freq": 110},
}


# Типы бонусов
POWERUP_TYPES = ["nitro", "shield", "repair"]

# Возможные значения монет
COIN_VALUES = [1, 1, 1, 2, 2, 5]


# ==========================================================
# ROAD — класс дороги
# ==========================================================

class Road:
    def __init__(self, W, H):
        self.W = W  # ширина окна
        self.H = H  # высота окна

        self.num_lanes = 5  # количество полос
        self.margin = 60    # отступ дороги от левого и правого края

        self.road_w = W - self.margin * 2  # ширина дороги
        self.lane_w = self.road_w // self.num_lanes  # ширина одной полосы

        self.scroll = 0     # отвечает за движение линий дороги
        self.line_h = 60    # высота одной дорожной линии
        self.line_gap = 40  # промежуток между линиями

        # BUMP — лежачий полицейский, который замедляет игрока
        self.bump_y = -200
        self.bump_active = False
        self.bump_timer = 0

        # NITRO STRIP — полоса нитро на дороге
        self.nitro_y = -300
        self.nitro_active = False
        self.nitro_timer = 0

    def lane_center(self, lane):
        # Возвращает x-координату центра выбранной полосы
        return self.margin + lane * self.lane_w + self.lane_w // 2

    def update(self, speed, dt):
        # Двигаем линии дороги вниз
        # Это создает эффект движения машины вперед
        self.scroll = (self.scroll + speed) % (self.line_h + self.line_gap)

        # Если bump активен, он движется вниз
        if self.bump_active:
            self.bump_y += speed
            self.bump_timer -= dt

            # Если время закончилось или bump ушел за экран — выключаем его
            if self.bump_timer <= 0 or self.bump_y > self.H + 40:
                self.bump_active = False

        # Если nitro strip активен, он тоже движется вниз
        if self.nitro_active:
            self.nitro_y += speed
            self.nitro_timer -= dt

            # Если время закончилось или nitro ушел за экран — выключаем
            if self.nitro_timer <= 0 or self.nitro_y > self.H + 40:
                self.nitro_active = False

    def try_spawn_event(self, game_time):
        # Случайное появление bump
        if not self.bump_active and random.random() < 0.003:
            self.bump_y = -40
            self.bump_active = True
            self.bump_timer = 8.0

        # Случайное появление nitro strip
        if not self.nitro_active and random.random() < 0.002:
            self.nitro_y = -40
            self.nitro_active = True
            self.nitro_timer = 8.0

    def draw(self, surface):
        # Рисуем основной прямоугольник дороги
        road_rect = pygame.Rect(self.margin, 0, self.road_w, self.H)
        pygame.draw.rect(surface, ROAD_DARK, road_rect)

        # Рисуем полосы дороги разными оттенками
        for lane in range(self.num_lanes):
            x = self.margin + lane * self.lane_w
            shade = ROAD_MID if lane % 2 == 0 else ROAD_DARK
            pygame.draw.rect(surface, shade, (x, 0, self.lane_w, self.H))

        # Рисуем движущиеся разделительные линии
        for lane in range(1, self.num_lanes):
            x = self.margin + lane * self.lane_w
            y = -self.scroll

            while y < self.H:
                pygame.draw.rect(surface, LANE_MARK, (x - 2, y, 4, self.line_h))
                y += self.line_h + self.line_gap

        # Рисуем края дороги
        pygame.draw.rect(surface, (200, 180, 220), (self.margin - 8, 0, 8, self.H))
        pygame.draw.rect(surface, (200, 180, 220), (self.margin + self.road_w, 0, 8, self.H))

        # Если bump активен — рисуем его
        if self.bump_active:
            by = int(self.bump_y)
            pygame.draw.rect(surface, GRAY, (self.margin, by, self.road_w, 18), border_radius=5)

            for i in range(self.num_lanes):
                cx = self.margin + i * self.lane_w + self.lane_w // 2
                pygame.draw.ellipse(surface, (80, 70, 90), (cx - 20, by + 2, 40, 14))

            font = pygame.font.Font(None, 20)
            lbl = font.render("BUMP", True, WHITE)
            surface.blit(lbl, lbl.get_rect(center=(self.margin + self.road_w // 2, by + 9)))

        # Если nitro strip активен — рисуем его
        if self.nitro_active:
            ny = int(self.nitro_y)

            strip = pygame.Surface((self.road_w, 22), pygame.SRCALPHA)
            strip.fill((255, 220, 0, 100))

            surface.blit(strip, (self.margin, ny))
            pygame.draw.rect(surface, GOLD, (self.margin, ny, self.road_w, 22), 2)

            font = pygame.font.Font(None, 20)
            lbl = font.render("NITRO STRIP", True, GOLD)
            surface.blit(lbl, lbl.get_rect(center=(self.margin + self.road_w // 2, ny + 11)))


# ==========================================================
# PLAYER CAR — машина игрока
# ==========================================================

class PlayerCar:
    def __init__(self, road, color_name="pink"):
        self.road = road
        self.lane = 2  # стартовая полоса — середина

        self.W = 32
        self.H = 54

        self.x = road.lane_center(self.lane)
        self.y = road.H - 120

        self.color = CAR_COLORS.get(color_name, CAR_COLORS["pink"])

        self.move_anim = 0
        self.shield_active = False
        self.invincible_timer = 0

    def move(self, direction):
        # direction = -1 — движение влево
        # direction = 1 — движение вправо
        new_lane = self.lane + direction

        # Проверяем, чтобы машина не выехала за дорогу
        if 0 <= new_lane < self.road.num_lanes:
            self.lane = new_lane
            self.move_anim = 0.15

    def update(self, dt, speed):
        # Получаем центр нужной полосы
        target_x = self.road.lane_center(self.lane)

        # Плавное движение машины к новой полосе
        self.x += (target_x - self.x) * min(1.0, dt * 18)

        # Уменьшаем таймер анимации движения
        if self.move_anim > 0:
            self.move_anim -= dt

        # Уменьшаем таймер неуязвимости
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

    def get_rect(self):
        # Прямоугольник машины для проверки столкновений
        return pygame.Rect(
            int(self.x) - self.W // 2,
            int(self.y) - self.H // 2,
            self.W,
            self.H
        )

    def draw(self, surface):
        # Если игрок временно неуязвим, машина мигает
        blink = (int(self.invincible_timer * 8) % 2 == 0) if self.invincible_timer > 0 else True

        if not blink:
            return

        x, y = int(self.x), int(self.y)
        col = self.color

        # Корпус машины
        body = pygame.Rect(x - 14, y - 24, 28, 48)
        pygame.draw.rect(surface, col, body, border_radius=8)

        # Крыша машины
        roof = pygame.Rect(x - 10, y - 18, 20, 22)

        # Делаем цвет крыши чуть светлее основного цвета
        roof_color = (
            min(col[0] + 40, 255),
            min(col[1] + 40, 255),
            min(col[2] + 40, 255),
        )

        pygame.draw.rect(surface, roof_color, roof, border_radius=5)

        # Стекло
        pygame.draw.rect(surface, (40, 190, 255), pygame.Rect(x - 9, y - 17, 18, 10), border_radius=3)

        # Передние фары
        pygame.draw.rect(surface, (255, 255, 120), (x - 12, y - 24, 10, 7), border_radius=3)
        pygame.draw.rect(surface, (255, 255, 120), (x + 2, y - 24, 10, 7), border_radius=3)

        # Задние фары
        pygame.draw.rect(surface, (255, 80, 80), (x - 12, y + 20, 10, 6), border_radius=2)
        pygame.draw.rect(surface, (255, 80, 80), (x + 2, y + 20, 10, 6), border_radius=2)

        # Колеса
        for wx, wy in [(-14, -12), (14, -12), (-14, 14), (14, 14)]:
            pygame.draw.circle(surface, (30, 20, 40), (x + wx, y + wy), 6)
            pygame.draw.circle(surface, (80, 70, 90), (x + wx, y + wy), 4)

        # Если активен shield, рисуем круг вокруг машины
        if self.shield_active:
            pygame.draw.circle(surface, (100, 200, 255), (x, y), 36, 3)


# ==========================================================
# TRAFFIC CAR — машины-враги
# ==========================================================

class TrafficCar:
    COLORS = [
        (200, 80, 80),
        (80, 150, 200),
        (100, 180, 100),
        (200, 160, 50),
        (160, 80, 200),
    ]

    def __init__(self, road, speed):
        self.road = road

        # Случайная полоса
        self.lane = random.randint(0, road.num_lanes - 1)
        self.x = road.lane_center(self.lane)

        # Машина появляется сверху
        self.y = -60

        # Скорость немного случайная
        self.speed = speed * random.uniform(0.7, 1.1)

        # Случайный цвет машины
        self.color = random.choice(self.COLORS)

        self.W = 30
        self.H = 50

    def update(self, dt):
        # Движение машины-врага вниз
        self.y += self.speed

    def get_rect(self):
        # Прямоугольник для столкновения
        return pygame.Rect(
            int(self.x) - self.W // 2,
            int(self.y) - self.H // 2,
            self.W,
            self.H
        )

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        col = self.color

        # Корпус машины
        pygame.draw.rect(surface, col, (x - 13, y - 23, 26, 46), border_radius=7)

        # Цвет крыши чуть светлее
        roof_color = (
            min(col[0] + 30, 255),
            min(col[1] + 30, 255),
            min(col[2] + 30, 255),
        )

        pygame.draw.rect(surface, roof_color, (x - 9, y - 17, 18, 20), border_radius=4)

        # Стекло
        pygame.draw.rect(surface, (200, 240, 255), (x - 8, y - 16, 16, 9), border_radius=2)

        # Фары
        pygame.draw.rect(surface, (255, 255, 100), (x - 11, y + 18, 8, 6), border_radius=2)
        pygame.draw.rect(surface, (255, 255, 100), (x + 3, y + 18, 8, 6), border_radius=2)

        # Колеса
        for wx, wy in [(-13, -10), (13, -10), (-13, 13), (13, 13)]:
            pygame.draw.circle(surface, (25, 20, 35), (x + wx, y + wy), 5)


# ==========================================================
# OBSTACLE — препятствия
# ==========================================================

class Obstacle:
    TYPES = ["pothole", "barrier"]

    def __init__(self, road, speed):
        self.road = road

        # Случайная полоса
        self.lane = random.randint(0, road.num_lanes - 1)
        self.x = road.lane_center(self.lane)

        # Появляется сверху
        self.y = -40

        # Скорость препятствия
        self.speed = speed * 0.5

        # Случайный тип: pothole или barrier
        self.kind = random.choice(self.TYPES)

        # Размер зависит от типа препятствия
        self.W = 36 if self.kind == "barrier" else 30
        self.H = 20 if self.kind == "barrier" else 22

    def update(self, dt):
        # Движение препятствия вниз
        self.y += self.speed

    def get_rect(self):
        # Прямоугольник для collision
        return pygame.Rect(
            int(self.x) - self.W // 2,
            int(self.y) - self.H // 2,
            self.W,
            self.H
        )

    def draw(self, surface):
        x, y = int(self.x), int(self.y)

        # Если препятствие — яма
        if self.kind == "pothole":
            pygame.draw.ellipse(surface, (15, 10, 25), (x - 15, y - 11, 30, 22))
            pygame.draw.ellipse(surface, (35, 25, 48), (x - 11, y - 8, 22, 16))

        # Если препятствие — барьер
        elif self.kind == "barrier":
            pygame.draw.rect(surface, (220, 60, 60), (x - 18, y - 9, 36, 18), border_radius=4)

            for i in range(3):
                sx = x - 15 + i * 15
                pygame.draw.rect(surface, WHITE, (sx, y - 9, 7, 18))


# ==========================================================
# COIN — монеты
# ==========================================================

class Coin:
    def __init__(self, road, speed):
        self.road = road

        # Случайная полоса
        self.lane = random.randint(0, road.num_lanes - 1)
        self.x = road.lane_center(self.lane)

        # Появляется сверху
        self.y = -20

        # Скорость монеты
        self.speed = speed * 0.5

        # Случайная ценность монеты
        self.value = random.choice(COIN_VALUES)

        # Для анимации монеты
        self.anim = random.uniform(0, math.pi * 2)

    def update(self, dt):
        # Монета движется вниз
        self.y += self.speed

        # Анимация монеты
        self.anim += dt * 4

    def get_rect(self):
        # Прямоугольник монеты для collision
        return pygame.Rect(int(self.x) - 12, int(self.y) - 12, 24, 24)

    def draw(self, surface):
        x, y = int(self.x), int(self.y)

        # bob дает легкое движение вверх-вниз
        bob = math.sin(self.anim) * 3

        # Монета с value 5 будет оранжевой
        col = GOLD if self.value <= 2 else ORANGE

        # Рисуем монету
        pygame.draw.circle(surface, col, (x, int(y + bob)), 11)
        pygame.draw.circle(surface, (255, 240, 120), (x - 2, int(y + bob) - 2), 5)

        # Пишем значение монеты
        font = pygame.font.Font(None, 16)
        lbl = font.render(str(self.value), True, (40, 20, 0))
        surface.blit(lbl, lbl.get_rect(center=(x, int(y + bob))))


# ==========================================================
# POWERUP — бонусы
# ==========================================================

class PowerUp:
    COLORS = {
        "nitro": (255, 200, 0),
        "shield": (100, 200, 255),
        "repair": (100, 255, 150),
    }

    def __init__(self, road, speed):
        self.road = road

        # Случайная полоса
        self.lane = random.randint(0, road.num_lanes - 1)
        self.x = road.lane_center(self.lane)

        # Появляется сверху
        self.y = -30

        # Скорость движения вниз
        self.speed = speed * 0.45

        # Случайный тип power-up
        self.kind = random.choice(POWERUP_TYPES)

        # Время жизни power-up
        self.lifetime = 8.0

        # Для анимации пульсации
        self.anim = 0.0

    def update(self, dt):
        # Двигаем power-up вниз
        self.y += self.speed

        # Обновляем анимацию
        self.anim += dt * 3

        # Уменьшаем время жизни
        self.lifetime -= dt

    def get_rect(self):
        # Прямоугольник для collision
        return pygame.Rect(int(self.x) - 16, int(self.y) - 16, 32, 32)

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        col = self.COLORS[self.kind]

        # Пульсация круга
        pulse = abs(math.sin(self.anim)) * 4

        # Рисуем power-up
        pygame.draw.circle(surface, col, (x, y), int(16 + pulse))
        pygame.draw.circle(surface, WHITE, (x, y), int(14 + pulse), 2)

        # Текст внутри power-up
        font = pygame.font.Font(None, 22)
        lbl = font.render(self.kind[:3].upper(), True, (20, 10, 30))
        surface.blit(lbl, lbl.get_rect(center=(x, y)))


# ==========================================================
# GAME SESSION — главный класс всей игры
# ==========================================================

class GameSession:
    def __init__(self, W, H, car_color, difficulty):
        self.W = W
        self.H = H

        # Создаем дорогу
        self.road = Road(W, H)

        # Создаем машину игрока
        self.player = PlayerCar(self.road, car_color)

        # Берем настройки сложности
        self.diff = DIFF_SETTINGS[difficulty]
        self.base_speed = self.diff["base_speed"]
        self.speed = self.base_speed

        # Очки, монеты, дистанция
        self.score = 0
        self.coins = 0
        self.distance = 0.0

        # Списки игровых объектов
        self.traffic = []
        self.obstacles = []
        self.coin_objs = []
        self.powerups = []

        # Активный power-up
        self.active_powerup = None
        self.powerup_timer = 0.0
        self.shield_active = False

        # Таймеры появления объектов
        self.traffic_timer = 0
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.powerup_spawn_timer = 0

        # Время игры и состояние
        self.game_time = 0.0
        self.alive = True

        # Таймер замедления от bump
        self.bump_slow_timer = 0.0

    def handle_input(self, keys):
        # Пока не используется, но можно было бы обрабатывать зажатые клавиши
        pass

    def on_key_down(self, key):
        # Движение влево
        if key in [pygame.K_LEFT, pygame.K_a]:
            self.player.move(-1)

        # Движение вправо
        elif key in [pygame.K_RIGHT, pygame.K_d]:
            self.player.move(1)

    def _safe_spawn_traffic(self):
        # Выбираем случайную полосу
        lane = random.randint(0, self.road.num_lanes - 1)

        # Создаем машину
        car = TrafficCar(self.road, self.speed)
        car.lane = lane
        car.x = self.road.lane_center(lane)

        # Если машина появляется слишком близко к игроку на той же полосе — не создаем
        if abs(car.y - self.player.y) < 120 and car.lane == self.player.lane:
            return None

        return car

    def _safe_spawn_obstacle(self):
        # Выбираем случайную полосу
        lane = random.randint(0, self.road.num_lanes - 1)

        # Создаем препятствие
        obs = Obstacle(self.road, self.speed)
        obs.lane = lane
        obs.x = self.road.lane_center(lane)

        # Если препятствие слишком близко к игроку — не создаем
        if obs.lane == self.player.lane and obs.y < self.player.y + 200:
            return None

        return obs

    def update(self, dt):
        # Если игрок уже проиграл, игру не обновляем
        if not self.alive:
            return

        # Увеличиваем время игры
        self.game_time += dt

        # Чем больше дистанция, тем выше плотность/сложность
        density = 1 + self.distance / 800

        # Текущая скорость зависит от базовой скорости и дистанции
        current_speed = self.speed * density

        # Если игрок попал на bump, скорость временно уменьшается
        if self.bump_slow_timer > 0:
            current_speed *= 0.5
            self.bump_slow_timer -= dt

        # Если активен nitro, скорость увеличивается
        if self.active_powerup == "nitro":
            current_speed *= 1.8

        # Обновляем дорогу
        self.road.update(current_speed, dt)

        # Пытаемся случайно создать события на дороге
        self.road.try_spawn_event(self.game_time)

        # Обновляем игрока
        self.player.update(dt, current_speed)

        # Увеличиваем дистанцию
        self.distance += current_speed * dt * 0.8

        # Считаем очки
        self.score = int(self.coins * 10 + self.distance * 0.5)

        # Обновление активного power-up
        if self.active_powerup:
            self.powerup_timer -= dt

            if self.powerup_timer <= 0:
                # Если закончился shield — выключаем щит
                if self.active_powerup == "shield":
                    self.player.shield_active = False
                    self.shield_active = False

                # Сбрасываем power-up
                self.active_powerup = None
                self.powerup_timer = 0

        # Чем больше дистанция, тем чаще появляются объекты
        freq_scale = max(0.4, 1 - self.distance / 1200)

        # =========================
        # СПАВН МАШИН-ВРАГОВ
        # =========================
        self.traffic_timer += 1

        if self.traffic_timer >= int(self.diff["traffic_freq"] * freq_scale):
            self.traffic_timer = 0
            traffic_car = self._safe_spawn_traffic()

            if traffic_car:
                self.traffic.append(traffic_car)

        # =========================
        # СПАВН ПРЕПЯТСТВИЙ
        # =========================
        self.obstacle_timer += 1

        if self.obstacle_timer >= int(self.diff["obstacle_freq"] * freq_scale):
            self.obstacle_timer = 0
            obstacle = self._safe_spawn_obstacle()

            if obstacle:
                self.obstacles.append(obstacle)

        # =========================
        # СПАВН МОНЕТ
        # =========================
        self.coin_timer += 1

        if self.coin_timer >= 60:
            self.coin_timer = 0
            self.coin_objs.append(Coin(self.road, current_speed))

        # =========================
        # СПАВН POWER-UP
        # =========================
        self.powerup_spawn_timer += 1

        if self.powerup_spawn_timer >= 300 and len(self.powerups) == 0 and not self.active_powerup:
            self.powerup_spawn_timer = 0
            self.powerups.append(PowerUp(self.road, current_speed))

        # Двигаем машины
        for traffic_car in self.traffic:
            traffic_car.update(dt)

        # Двигаем препятствия
        for obstacle in self.obstacles:
            obstacle.update(dt)

        # Двигаем монеты
        for coin in self.coin_objs:
            coin.update(dt)

        # Двигаем power-up
        for powerup in self.powerups:
            powerup.update(dt)

        # Удаляем объекты, которые ушли за экран
        self.traffic = [t for t in self.traffic if t.y < self.H + 80]
        self.obstacles = [o for o in self.obstacles if o.y < self.H + 80]
        self.coin_objs = [c for c in self.coin_objs if c.y < self.H + 80]
        self.powerups = [p for p in self.powerups if p.y < self.H + 80 and p.lifetime > 0]

        # Получаем прямоугольник игрока для столкновений
        player_rect = self.player.get_rect()

        # =========================
        # СБОР МОНЕТ
        # =========================
        for coin in self.coin_objs[:]:
            if player_rect.colliderect(coin.get_rect()):
                self.coins += coin.value
                self.score += coin.value * 10
                self.coin_objs.remove(coin)

        # =========================
        # СБОР POWER-UP
        # =========================
        for powerup in self.powerups[:]:
            if player_rect.colliderect(powerup.get_rect()):
                self.apply_powerup(powerup.kind)
                self.powerups.remove(powerup)

        # Если игрок временно неуязвим, collision с врагами не проверяем
        if self.player.invincible_timer > 0:
            return

        # =========================
        # СТОЛКНОВЕНИЕ С МАШИНАМИ
        # =========================
        for traffic_car in self.traffic[:]:
            if player_rect.colliderect(traffic_car.get_rect()):

                # Если есть щит, удар не убивает игрока
                if self.shield_active:
                    self.shield_active = False
                    self.player.shield_active = False
                    self.active_powerup = None
                    self.powerup_timer = 0
                    self.player.invincible_timer = 2.0

                else:
                    # Если щита нет — game over
                    self.alive = False

                return

        # =========================
        # СТОЛКНОВЕНИЕ С ПРЕПЯТСТВИЯМИ
        # =========================
        for obstacle in self.obstacles[:]:
            if player_rect.colliderect(obstacle.get_rect()):

                # Если есть shield, препятствие убирается
                if self.shield_active:
                    self.shield_active = False
                    self.player.shield_active = False
                    self.active_powerup = None
                    self.powerup_timer = 0
                    self.obstacles.remove(obstacle)
                    self.player.invincible_timer = 2.0

                # Если активен repair, препятствие убирается
                elif self.active_powerup == "repair":
                    self.obstacles.remove(obstacle)
                    self.active_powerup = None
                    self.powerup_timer = 0

                else:
                    # Если защиты нет — game over
                    self.alive = False

                return

        # =========================
        # ПРОВЕРКА BUMP
        # =========================
        if self.road.bump_active:
            bump_rect = pygame.Rect(
                self.road.margin,
                int(self.road.bump_y) - 9,
                self.road.road_w,
                18
            )

            # Если игрок наехал на bump — замедляем
            if player_rect.colliderect(bump_rect):
                self.bump_slow_timer = 1.5

        # =========================
        # ПРОВЕРКА NITRO STRIP
        # =========================
        if self.road.nitro_active:
            nitro_rect = pygame.Rect(
                self.road.margin,
                int(self.road.nitro_y),
                self.road.road_w,
                22
            )

            # Если игрок наехал на nitro strip — активируем nitro
            if player_rect.colliderect(nitro_rect):
                if not self.active_powerup:
                    self.apply_powerup("nitro")

    def apply_powerup(self, kind):
        # Сохраняем активный power-up
        self.active_powerup = kind
        self.powerup_timer = 4.0

        # Shield включает защиту
        if kind == "shield":
            self.shield_active = True
            self.player.shield_active = True

        # Repair работает почти сразу и убирает препятствие при столкновении
        elif kind == "repair":
            self.powerup_timer = 0.1

        # Nitro ускоряет игрока на 4 секунды
        elif kind == "nitro":
            self.powerup_timer = 4.0

    def draw(self, surface):
        # Сначала рисуем дорогу
        self.road.draw(surface)

        # Потом машины-враги
        for traffic_car in self.traffic:
            traffic_car.draw(surface)

        # Потом препятствия
        for obstacle in self.obstacles:
            obstacle.draw(surface)

        # Потом монеты
        for coin in self.coin_objs:
            coin.draw(surface)

        # Потом power-up
        for powerup in self.powerups:
            powerup.draw(surface)

        # Игрок рисуется последним, чтобы быть сверху всех объектов
        self.player.draw(surface)