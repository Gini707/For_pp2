import pygame  # библиотека для графики, рисования объектов и работы с pygame.Rect
import random  # нужен для случайного выбора еды, power-up и свободных клеток
from config import *  # импортируем все настройки из config.py: размеры, цвета, скорость и т.д.


class Snake:
    def __init__(self, color):
        self.color = color  # сохраняем цвет змейки
        self.reset()  # создаем начальное состояние змейки

    def reset(self):
        cx = GRID_COLS // 2  # центр поля по колонкам
        cy = GRID_ROWS // 2  # центр поля по строкам

        # тело змейки: голова в центре, остальные части слева от головы
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]

        self.direction = (1, 0)  # текущее направление движения: вправо
        self.next_direction = (1, 0)  # следующее направление, которое применится при движении
        self.grew = False  # флаг: должна ли змейка вырасти после еды

    def set_direction(self, direction):
        # проверяем, чтобы змейка не могла резко развернуться назад на 180 градусов
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction  # сохраняем новое направление

    def move(self):
        self.direction = self.next_direction  # применяем новое направление

        # считаем новую голову змейки
        head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1]
        )

        self.body.insert(0, head)  # добавляем новую голову в начало списка

        if self.grew:
            self.grew = False  # если змейка должна была вырасти, хвост не удаляем
        else:
            self.body.pop()  # если роста нет, удаляем хвост

    def grow(self):
        self.grew = True  # включаем рост змейки на следующий ход

    def shorten(self, amount=2):
        # уменьшает змейку, например когда она съела poison
        for _ in range(amount):
            if len(self.body) > 1:  # не даем удалить змейку полностью
                self.body.pop()

    @property
    def head(self):
        return self.body[0]  # голова змейки — первый элемент списка body

    def collides_self(self):
        return self.head in self.body[1:]  # проверка столкновения головы с телом

    def collides_wall(self):
        x, y = self.head  # координаты головы
        return x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS  # проверка выхода за поле

    def draw(self, surface):
        # рисуем каждый сегмент змейки
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(
                segment[0] * CELL_SIZE,  # x в пикселях
                segment[1] * CELL_SIZE,  # y в пикселях
                CELL_SIZE,  # ширина клетки
                CELL_SIZE   # высота клетки
            )

            if i == 0:
                # голову делаем светлее, чтобы она отличалась от тела
                color = tuple(min(c + 60, 255) for c in self.color)
            else:
                # остальные сегменты обычного цвета
                color = self.color

            pygame.draw.rect(surface, color, rect)  # рисуем сегмент змейки
            pygame.draw.rect(surface, BLACK, rect, 1)  # рисуем черную рамку вокруг сегмента


class FoodItem:
    def __init__(self, pos, kind, spawn_time):
        self.pos = pos  # позиция еды на сетке
        self.kind = kind  # тип еды: normal, bonus или poison
        self.spawn_time = spawn_time  # время появления еды
        self.color = FOOD_COLORS[kind]  # цвет еды по типу
        self.points = FOOD_POINTS.get(kind, 0)  # сколько очков дает еда

    def is_expired(self, now):
        # проверка: прошло ли время жизни еды
        return now - self.spawn_time > FOOD_DISAPPEAR_TIME

    def draw(self, surface):
        x, y = self.pos  # координаты еды на сетке

        rect = pygame.Rect(
            x * CELL_SIZE + 2,  # x в пикселях с маленьким отступом
            y * CELL_SIZE + 2,  # y в пикселях с маленьким отступом
            CELL_SIZE - 4,  # ширина еды чуть меньше клетки
            CELL_SIZE - 4   # высота еды чуть меньше клетки
        )

        pygame.draw.ellipse(surface, self.color, rect)  # рисуем еду как круг/овал


class PowerUp:
    def __init__(self, pos, kind, spawn_time):
        self.pos = pos  # позиция power-up на сетке
        self.kind = kind  # тип power-up: speed, slow или shield
        self.spawn_time = spawn_time  # время появления power-up
        self.color = POWERUP_COLORS[kind]  # цвет power-up по типу

    def is_expired(self, now):
        # проверка: исчез ли power-up по времени
        return now - self.spawn_time > POWERUP_FIELD_TIME

    def draw(self, surface):
        x, y = self.pos  # координаты power-up на сетке

        # центр клетки в пикселях
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = y * CELL_SIZE + CELL_SIZE // 2

        # точки ромба
        points = [
            (cx, cy - CELL_SIZE // 2 + 2),
            (cx + CELL_SIZE // 2 - 2, cy),
            (cx, cy + CELL_SIZE // 2 - 2),
            (cx - CELL_SIZE // 2 + 2, cy),
        ]

        pygame.draw.polygon(surface, self.color, points)  # рисуем power-up как ромб


class Game:
    def __init__(self, settings, player_id, personal_best):
        self.settings = settings  # настройки игры: цвет змейки, сетка, звук и т.д.
        self.player_id = player_id  # id игрока из базы данных
        self.personal_best = personal_best  # лучший результат игрока

        self.snake = Snake(tuple(settings["snake_color"]))  # создаем змейку с цветом из настроек

        self.score = 0  # текущий счет
        self.level = 1  # начальный уровень
        self.speed = BASE_SPEED  # начальная скорость змейки

        self.foods = []  # список еды на поле
        self.powerup = None  # текущий power-up на поле
        self.obstacles = set()  # препятствия, set нужен чтобы быстро проверять столкновения

        self.shield_active = False  # активен ли щит
        self.active_effect = None  # текущий активный эффект: speed, slow или shield
        self.effect_end_time = 0  # время окончания эффекта

        self.move_accumulator = 0  # накапливает время для движения змейки
        self.over = False  # True значит игра закончилась

        self._spawn_food()  # сразу создаем первую еду

    def _occupied(self):
        # собирает все занятые клетки, чтобы туда не ставить еду или power-up
        occupied = set(self.snake.body) | self.obstacles

        for food in self.foods:
            occupied.add(food.pos)  # добавляем позиции еды

        if self.powerup:
            occupied.add(self.powerup.pos)  # добавляем позицию power-up

        return occupied

    def _random_free_cell(self):
        occupied = self._occupied()  # получаем занятые клетки

        free = []  # список свободных клеток

        for x in range(GRID_COLS):
            for y in range(GRID_ROWS):
                if (x, y) not in occupied:
                    free.append((x, y))  # добавляем свободную клетку

        if not free:
            return None  # если свободных клеток нет

        return random.choice(free)  # выбираем случайную свободную клетку

    def _spawn_food(self):
        now = pygame.time.get_ticks()  # текущее время в миллисекундах
        pos = self._random_free_cell()  # случайная свободная клетка

        if pos is None:
            return  # если места нет, еду не создаем

        kind = random.choices(
            ["normal", "bonus", "poison"],  # типы еды
            weights=[70, 20, 10]  # шанс: normal 70%, bonus 20%, poison 10%
        )[0]

        self.foods.append(FoodItem(pos, kind, now))  # добавляем еду в список

    def _maybe_spawn_powerup(self):
        if self.powerup is not None:
            return  # если power-up уже есть на поле, новый не создаем

        if random.random() < 0.01:  # шанс появления power-up — 1% за update
            pos = self._random_free_cell()  # ищем свободную клетку

            if pos is None:
                return

            kind = random.choice(["speed", "slow", "shield"])  # случайный тип power-up
            self.powerup = PowerUp(pos, kind, pygame.time.get_ticks())  # создаем power-up

    def _spawn_obstacles(self):
        if self.level < OBSTACLE_START_LEVEL:
            return  # препятствия появляются только с определенного уровня

        count = OBSTACLES_PER_LEVEL * (self.level - OBSTACLE_START_LEVEL + 1)  # количество препятствий
        head = self.snake.head  # позиция головы змейки

        attempts = 0  # счетчик попыток

        while len(self.obstacles) < count and attempts < count * 20:
            attempts += 1

            pos = self._random_free_cell()  # ищем свободную клетку

            if pos is None:
                break

            # не ставим препятствие слишком близко к голове змейки
            if abs(pos[0] - head[0]) <= 3 and abs(pos[1] - head[1]) <= 3:
                continue

            self.obstacles.add(pos)  # добавляем препятствие

    def _apply_powerup(self, kind):
        now = pygame.time.get_ticks()  # текущее время

        self.active_effect = kind  # сохраняем активный эффект

        if kind == "speed":
            # speed увеличивает скорость
            self.speed = BASE_SPEED + (self.level - 1) * SPEED_INCREMENT + 4
            self.effect_end_time = now + POWERUP_EFFECT_TIME

        elif kind == "slow":
            # slow уменьшает скорость, но не ниже 2
            self.speed = max(2, BASE_SPEED + (self.level - 1) * SPEED_INCREMENT - 4)
            self.effect_end_time = now + POWERUP_EFFECT_TIME

        elif kind == "shield":
            # shield защищает от одного столкновения
            self.shield_active = True
            self.effect_end_time = 0

    def _clear_effect(self):
        if self.active_effect in ["speed", "slow"]:
            # возвращаем обычную скорость по уровню
            self.speed = BASE_SPEED + (self.level - 1) * SPEED_INCREMENT

        self.active_effect = None  # очищаем эффект

    def handle_event(self, event):
        # обработка нажатий клавиш
        if event.type == pygame.KEYDOWN:
            keys = {
                pygame.K_UP: (0, -1),      # стрелка вверх
                pygame.K_w: (0, -1),       # W вверх
                pygame.K_DOWN: (0, 1),     # стрелка вниз
                pygame.K_s: (0, 1),        # S вниз
                pygame.K_LEFT: (-1, 0),    # стрелка влево
                pygame.K_a: (-1, 0),       # A влево
                pygame.K_RIGHT: (1, 0),    # стрелка вправо
                pygame.K_d: (1, 0),        # D вправо
            }

            if event.key in keys:
                self.snake.set_direction(keys[event.key])  # меняем направление змейки

    def update(self, dt):
        if self.over:
            return  # если игра окончена, ничего не обновляем

        now = pygame.time.get_ticks()  # текущее время

        self._maybe_spawn_powerup()  # иногда создаем power-up

        if self.active_effect in ["speed", "slow"] and now >= self.effect_end_time:
            self._clear_effect()  # если время эффекта закончилось, очищаем его

        self.foods = [food for food in self.foods if not food.is_expired(now)]  # удаляем старую еду

        if not self.foods:
            self._spawn_food()  # если еды нет, создаем новую

        if self.powerup and self.powerup.is_expired(now):
            self.powerup = None  # удаляем power-up, если он исчез по времени

        self.move_accumulator += dt  # добавляем прошедшее время
        move_interval = 1000 / self.speed  # сколько миллисекунд ждать до следующего движения

        if self.move_accumulator < move_interval:
            return  # если еще рано двигаться, выходим

        self.move_accumulator -= move_interval  # уменьшаем накопленное время

        self.snake.move()  # двигаем змейку
        head = self.snake.head  # новая позиция головы

        wall_hit = self.snake.collides_wall()  # проверка удара о стену
        self_hit = self.snake.collides_self()  # проверка удара в себя
        obstacle_hit = head in self.obstacles  # проверка удара в препятствие

        if wall_hit or self_hit or obstacle_hit:
            if self.shield_active:
                # если щит активен, он спасает от столкновения
                self.shield_active = False
                self.active_effect = None

                if wall_hit:
                    # если ударились об стену, возвращаем голову в границы поля
                    x = max(0, min(GRID_COLS - 1, head[0]))
                    y = max(0, min(GRID_ROWS - 1, head[1]))
                    self.snake.body[0] = (x, y)

                elif obstacle_hit:
                    # если ударились в препятствие, щит удаляет препятствие
                    self.obstacles.discard(head)

            else:
                self.over = True  # если щита нет, игра заканчивается
                return

        for food in self.foods[:]:
            if food.pos == head:
                self.foods.remove(food)  # удаляем съеденную еду

                if food.kind == "poison":
                    self.snake.shorten(2)  # poison уменьшает змейку

                    if len(self.snake.body) <= 1:
                        self.over = True  # если змейка стала слишком маленькой — game over
                        return

                else:
                    self.score += food.points  # добавляем очки
                    self.snake.grow()  # змейка растет

                    if self.score >= self.level * LEVEL_UP_SCORE:
                        self.level += 1  # повышаем уровень
                        self.speed = BASE_SPEED + (self.level - 1) * SPEED_INCREMENT  # повышаем скорость
                        self._spawn_obstacles()  # добавляем препятствия

                self._spawn_food()  # создаем новую еду
                break

        if self.powerup and self.powerup.pos == head:
            self._apply_powerup(self.powerup.kind)  # активируем power-up
            self.powerup = None  # убираем power-up с поля

    def draw(self, surface):
        surface.fill(BG_COLOR)  # очищаем экран цветом фона

        if self.settings.get("grid_overlay"):
            # рисуем вертикальные линии сетки
            for x in range(0, WINDOW_WIDTH, CELL_SIZE):
                pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))

            # рисуем горизонтальные линии сетки
            for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
                pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

        for obstacle in self.obstacles:
            rect = pygame.Rect(
                obstacle[0] * CELL_SIZE,
                obstacle[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(surface, LIGHT_GRAY, rect)  # рисуем препятствие
            pygame.draw.rect(surface, GRAY, rect, 2)  # рамка препятствия

        for food in self.foods:
            food.draw(surface)  # рисуем всю еду

        if self.powerup:
            self.powerup.draw(surface)  # рисуем power-up, если он есть

        self.snake.draw(surface)  # рисуем змейку
        self._draw_hud(surface)  # рисуем счет, уровень и power-up status

    def _draw_hud(self, surface):
        font_sm = pygame.font.SysFont("consolas", 18)  # маленький шрифт
        font_md = pygame.font.SysFont("consolas", 22, bold=True)  # средний жирный шрифт

        hud = [
            f"Score: {self.score}",  # очки
            f"Level: {self.level}",  # уровень
            f"Best: {self.personal_best}",  # лучший результат
        ]

        for i, text in enumerate(hud):
            surf = font_md.render(text, True, WHITE)  # создаем текст
            surface.blit(surf, (10, 10 + i * 28))  # рисуем текст слева сверху

        if self.shield_active:
            text = "SHIELD ACTIVE"  # если активен щит
            color = YELLOW

        elif self.active_effect == "speed":
            text = "SPEED BOOST"  # если активен speed
            color = CYAN

        elif self.active_effect == "slow":
            text = "SLOW MOTION"  # если активен slow
            color = PURPLE

        else:
            text = "Power-up: none"  # если power-up нет
            color = LIGHT_GRAY

        surf = font_sm.render(text, True, color)  # создаем текст статуса
        surface.blit(surf, (WINDOW_WIDTH - surf.get_width() - 10, 10))  # рисуем справа сверху