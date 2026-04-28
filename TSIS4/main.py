import sys  # нужен для полного выхода из программы через sys.exit()
import pygame  # библиотека для создания окна, кнопок, текста и обработки событий
from config import *  # импортируем все настройки: цвета, размеры окна, FPS и т.д.
from game import Game  # импортируем главный класс игры Snake


# Пробуем подключить базу данных
try:
    import db  # импорт файла db.py
    db.init_db()  # создаем/инициализируем таблицы базы данных
    DB_AVAILABLE = True  # если ошибок нет, база доступна
    print("DB connected OK")
except Exception as e:
    DB_AVAILABLE = False  # если ошибка, игра работает без базы
    print(f"DB not available: {e}")


def draw_background(surface):
    # Заливает весь экран цветом фона
    surface.fill(BG_COLOR)


def draw_text(surface, text, font, color, x, y, center=True):
    # Создаем картинку текста
    surf = font.render(text, True, color)

    # Получаем прямоугольник текста
    rect = surf.get_rect()

    # Если center=True, текст центрируется по x
    if center:
        rect.centerx = x
        rect.y = y
    else:
        # Если center=False, текст начинается с координаты x
        rect.x = x
        rect.y = y

    # Отображаем текст на экране
    surface.blit(surf, rect)

    # Возвращаем rect, если потом нужно проверить позицию текста
    return rect


def draw_button(surface, text, font, rect, hover=False):
    # Если мышка наведена — кнопка светлее
    color = LIGHT_GRAY if hover else GRAY

    # Рисуем фон кнопки
    pygame.draw.rect(surface, color, rect, border_radius=8)

    # Рисуем белую рамку кнопки
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)

    # Создаем текст кнопки
    txt_surf = font.render(text, True, WHITE)

    # Центрируем текст внутри кнопки
    txt_rect = txt_surf.get_rect(center=rect.center)

    # Отображаем текст кнопки
    surface.blit(txt_surf, txt_rect)


def make_button(text, font, cx, y, w=220, h=48):
    # Создаем прямоугольник кнопки
    rect = pygame.Rect(0, y, w, h)

    # Ставим кнопку по центру экрана
    rect.centerx = cx

    # Возвращаем кнопку
    return rect


class MainMenu:
    def __init__(self, surface, clock, settings):
        self.surface = surface  # экран, на котором рисуем меню
        self.clock = clock  # clock контролирует FPS
        self.settings = settings  # настройки игры

        # Шрифты для заголовка, кнопок и маленького текста
        self.font_title = pygame.font.SysFont("consolas", 52, bold=True)
        self.font_btn = pygame.font.SysFont("consolas", 26)
        self.font_sm = pygame.font.SysFont("consolas", 20)

        self.username = ""  # имя игрока
        self.typing = True  # сначала игрок вводит имя

        cx = WINDOW_WIDTH // 2  # центр экрана по x

        # Создаем кнопки меню
        self.btn_play = make_button("PLAY", self.font_btn, cx, 330)
        self.btn_lb = make_button("LEADERBOARD", self.font_btn, cx, 395)
        self.btn_settings = make_button("SETTINGS", self.font_btn, cx, 460)
        self.btn_quit = make_button("QUIT", self.font_btn, cx, 525)

    def run(self):
        # Бесконечный цикл меню
        while True:
            dt = self.clock.tick(FPS)  # ограничиваем FPS
            mouse = pygame.mouse.get_pos()  # получаем позицию мышки

            # Обрабатываем все события
            for event in pygame.event.get():

                # Если нажали крестик окна
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Ввод имени игрока
                if event.type == pygame.KEYDOWN and self.typing:

                    # Backspace удаляет последний символ
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]

                    # Enter подтверждает имя
                    elif event.key == pygame.K_RETURN:
                        if self.username.strip():
                            self.typing = False

                    # Обычный ввод символов
                    elif len(self.username) < 20 and event.unicode.isprintable():
                        self.username += event.unicode

                # После ввода имени можно нажимать кнопки мышкой
                if event.type == pygame.MOUSEBUTTONDOWN and not self.typing:

                    # Кнопка PLAY запускает игру
                    if self.btn_play.collidepoint(mouse):
                        return "play", self.username.strip()

                    # Кнопка LEADERBOARD открывает таблицу лидеров
                    if self.btn_lb.collidepoint(mouse):
                        return "leaderboard", self.username.strip()

                    # Кнопка SETTINGS открывает настройки
                    if self.btn_settings.collidepoint(mouse):
                        return "settings", self.username.strip()

                    # Кнопка QUIT закрывает игру
                    if self.btn_quit.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()

            # Рисуем фон меню
            draw_background(self.surface)

            # Рисуем заголовок SNAKE
            draw_text(self.surface, "SNAKE", self.font_title, GREEN,
                      WINDOW_WIDTH // 2, 60)

            # Если вводим имя — пишем Enter username
            # Если имя уже введено — показываем Player: username
            prompt = "Enter username:" if self.typing else f"Player: {self.username}"
            color = YELLOW if self.typing else WHITE

            draw_text(self.surface, prompt, self.font_sm, color, WINDOW_WIDTH // 2, 180)

            # Если игрок еще вводит имя
            if self.typing:
                # Поле ввода имени
                input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 140, 210, 280, 40)

                # Рисуем поле ввода
                pygame.draw.rect(self.surface, GRAY, input_rect, border_radius=6)
                pygame.draw.rect(self.surface, WHITE, input_rect, 2, border_radius=6)

                # Показываем введенное имя и мигающий курсор |
                name_surf = self.font_sm.render(self.username + "|", True, WHITE)
                self.surface.blit(name_surf, (input_rect.x + 8, input_rect.y + 8))

                # Подсказка
                hint = self.font_sm.render("Press Enter to confirm", True, LIGHT_GRAY)
                self.surface.blit(hint, hint.get_rect(centerx=WINDOW_WIDTH // 2, y=260))

            else:
                # Если имя уже введено — показываем кнопки меню
                for btn, label in [
                    (self.btn_play, "PLAY"),
                    (self.btn_lb, "LEADERBOARD"),
                    (self.btn_settings, "SETTINGS"),
                    (self.btn_quit, "QUIT"),
                ]:
                    draw_button(self.surface, label, self.font_btn, btn,
                                hover=btn.collidepoint(mouse))

            # Обновляем экран
            pygame.display.flip()


class GameOverScreen:
    def __init__(self, surface, clock, score, level, personal_best):
        self.surface = surface  # экран
        self.clock = clock  # clock для FPS

        self.score = score  # финальный счет
        self.level = level  # достигнутый уровень
        self.personal_best = personal_best  # лучший результат игрока

        # Шрифты
        self.font_title = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 26)
        self.font_btn = pygame.font.SysFont("consolas", 24)

        cx = WINDOW_WIDTH // 2

        # Кнопка перезапуска
        self.btn_retry = make_button("RETRY", self.font_btn, cx, 380)

        # Кнопка возврата в главное меню
        self.btn_menu = make_button("MAIN MENU", self.font_btn, cx, 445)

    def run(self):
        # Бесконечный цикл экрана Game Over
        while True:
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()

            # Обработка событий
            for event in pygame.event.get():

                # Закрытие окна
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Клик мышкой по кнопкам
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Если нажали Retry — начать заново
                    if self.btn_retry.collidepoint(mouse):
                        return "retry"

                    # Если нажали Main Menu — выйти в меню
                    if self.btn_menu.collidepoint(mouse):
                        return "menu"

            # Рисуем фон
            draw_background(self.surface)

            # Заголовок GAME OVER
            draw_text(self.surface, "GAME OVER", self.font_title, RED,
                      WINDOW_WIDTH // 2, 80)

            # Показываем финальный score
            draw_text(self.surface, f"Score: {self.score}", self.font_md, WHITE,
                      WINDOW_WIDTH // 2, 200)

            # Показываем уровень
            draw_text(self.surface, f"Level reached: {self.level}", self.font_md, WHITE,
                      WINDOW_WIDTH // 2, 240)

            # Если score больше или равен personal_best, подсвечиваем желтым
            best_color = YELLOW if self.score >= self.personal_best else LIGHT_GRAY

            # Показываем personal best
            draw_text(self.surface, f"Personal best: {self.personal_best}", self.font_md,
                      best_color, WINDOW_WIDTH // 2, 280)

            # Если новый рекорд — показываем NEW RECORD
            if self.score >= self.personal_best:
                draw_text(self.surface, "NEW RECORD!", self.font_md, YELLOW,
                          WINDOW_WIDTH // 2, 320)

            # Рисуем кнопки Retry и Main Menu
            for btn, label in [(self.btn_retry, "RETRY"), (self.btn_menu, "MAIN MENU")]:
                draw_button(self.surface, label, self.font_btn, btn,
                            hover=btn.collidepoint(mouse))

            # Обновляем экран
            pygame.display.flip()

class GameOverScreen:
    def __init__(self, surface, clock, score, level, personal_best):
        self.surface = surface  # экран, на котором рисуется Game Over
        self.clock = clock  # clock нужен для FPS
        self.score = score  # финальный счет игрока
        self.level = level  # уровень, до которого дошел игрок
        self.personal_best = personal_best  # лучший результат игрока

        # шрифты для заголовка, текста и кнопок
        self.font_title = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 26)
        self.font_btn = pygame.font.SysFont("consolas", 24)

        cx = WINDOW_WIDTH // 2  # центр экрана по X

        # кнопка заново начать игру
        self.btn_retry = make_button("RETRY", self.font_btn, cx, 380)

        # кнопка вернуться в главное меню
        self.btn_menu = make_button("MAIN MENU", self.font_btn, cx, 445)

    def run(self):
        # отдельный цикл экрана Game Over
        while True:
            self.clock.tick(FPS)  # ограничиваем FPS
            mouse = pygame.mouse.get_pos()  # позиция мышки

            # обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # если нажали мышкой
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_retry.collidepoint(mouse):
                        return "retry"  # возвращаем команду перезапуска

                    if self.btn_menu.collidepoint(mouse):
                        return "menu"  # возвращаем команду меню

            draw_background(self.surface)  # рисуем фон

            # заголовок GAME OVER
            draw_text(self.surface, "GAME OVER", self.font_title, RED,
                      WINDOW_WIDTH // 2, 80)

            # показываем счет
            draw_text(self.surface, f"Score: {self.score}", self.font_md, WHITE,
                      WINDOW_WIDTH // 2, 200)

            # показываем уровень
            draw_text(self.surface, f"Level reached: {self.level}", self.font_md, WHITE,
                      WINDOW_WIDTH // 2, 240)

            # если новый рекорд — personal best будет желтым
            best_color = YELLOW if self.score >= self.personal_best else LIGHT_GRAY

            # показываем лучший результат
            draw_text(self.surface, f"Personal best: {self.personal_best}", self.font_md,
                      best_color, WINDOW_WIDTH // 2, 280)

            # если счет больше/равен рекорду — пишем NEW RECORD
            if self.score >= self.personal_best:
                draw_text(self.surface, "NEW RECORD!", self.font_md, YELLOW,
                          WINDOW_WIDTH // 2, 320)

            # рисуем кнопки Retry и Main Menu
            for btn, label in [(self.btn_retry, "RETRY"), (self.btn_menu, "MAIN MENU")]:
                draw_button(self.surface, label, self.font_btn, btn,
                            hover=btn.collidepoint(mouse))

            pygame.display.flip()  # обновляем экран


class LeaderboardScreen:
    def __init__(self, surface, clock):
        self.surface = surface  # экран
        self.clock = clock  # clock для FPS

        # шрифты для таблицы лидеров
        self.font_title = pygame.font.SysFont("consolas", 40, bold=True)
        self.font_hdr = pygame.font.SysFont("consolas", 20, bold=True)
        self.font_row = pygame.font.SysFont("consolas", 18)
        self.font_btn = pygame.font.SysFont("consolas", 24)

        # кнопка назад
        self.btn_back = make_button("BACK", self.font_btn, WINDOW_WIDTH // 2, 540)

        # список строк leaderboard
        self.rows = []

        # если база данных работает, берем top 10 игроков
        if DB_AVAILABLE:
            try:
                self.rows = db.get_top10()
            except Exception:
                pass

    def run(self):
        # цикл экрана leaderboard
        while True:
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # если нажали BACK — возвращаемся назад
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_back.collidepoint(mouse):
                        return

            draw_background(self.surface)

            # заголовок
            draw_text(self.surface, "LEADERBOARD", self.font_title, YELLOW,
                      WINDOW_WIDTH // 2, 30)

            # заголовки таблицы
            headers = ["#", "Username", "Score", "Level", "Date"]
            col_x = [30, 80, 320, 430, 530]
            y = 100

            for i, h in enumerate(headers):
                surf = self.font_hdr.render(h, True, CYAN)
                self.surface.blit(surf, (col_x[i], y))

            # линия под заголовками
            pygame.draw.line(self.surface, LIGHT_GRAY, (20, y + 24), (WINDOW_WIDTH - 20, y + 24), 1)

            # выводим игроков из базы данных
            for rank, row in enumerate(self.rows, 1):
                y2 = 130 + (rank - 1) * 34

                # первое место желтым
                color = YELLOW if rank == 1 else WHITE

                vals = [
                    str(rank),  # место
                    row["username"][:16],  # имя игрока
                    str(row["score"]),  # score
                    str(row["level_reached"]),  # уровень
                    row["date"],  # дата
                ]

                # рисуем каждую колонку
                for i, v in enumerate(vals):
                    surf = self.font_row.render(v, True, color)
                    self.surface.blit(surf, (col_x[i], y2))

            # если записей нет
            if not self.rows:
                draw_text(self.surface, "No records yet", self.font_hdr, LIGHT_GRAY,
                          WINDOW_WIDTH // 2, 200)

            # кнопка назад
            draw_button(self.surface, "BACK", self.font_btn, self.btn_back,
                        hover=self.btn_back.collidepoint(mouse))

            pygame.display.flip()


class SettingsScreen:
    def __init__(self, surface, clock, settings):
        self.surface = surface  # экран
        self.clock = clock  # clock для FPS

        # копируем настройки, чтобы менять их внутри settings screen
        self.settings = dict(settings)

        # шрифты
        self.font_title = pygame.font.SysFont("consolas", 40, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 24)
        self.font_btn = pygame.font.SysFont("consolas", 22)

        cx = WINDOW_WIDTH // 2

        # кнопка включения/выключения сетки
        self.btn_grid = make_button("", self.font_btn, cx + 120, 200, 100, 40)

        # кнопка включения/выключения звука
        self.btn_sound = make_button("", self.font_btn, cx + 120, 260, 100, 40)

        # кнопки изменения цвета змейки RGB
        self.btn_color_r = make_button("Red+", self.font_btn, 160, 340, 90, 36)
        self.btn_color_g = make_button("Grn+", self.font_btn, 270, 340, 90, 36)
        self.btn_color_b = make_button("Blu+", self.font_btn, 380, 340, 90, 36)
        self.btn_color_rm = make_button("Red-", self.font_btn, 160, 384, 90, 36)
        self.btn_color_gm = make_button("Grn-", self.font_btn, 270, 384, 90, 36)
        self.btn_color_bm = make_button("Blu-", self.font_btn, 380, 384, 90, 36)

        # кнопка сохранения настроек
        self.btn_save = make_button("SAVE & BACK", self.font_btn, cx, 490, 240, 48)

    def _toggle(self, key):
        # меняет True на False и наоборот
        self.settings[key] = not self.settings[key]

    def _clamp_color(self, idx, delta):
        # берем цвет змейки как список [R, G, B]
        c = list(self.settings["snake_color"])

        # меняем один канал цвета, но не даем выйти за 0–255
        c[idx] = max(0, min(255, c[idx] + delta))

        # сохраняем новый цвет обратно
        self.settings["snake_color"] = c

    def run(self):
        # цикл экрана настроек
        while True:
            self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # обработка кликов по настройкам
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_grid.collidepoint(mouse):
                        self._toggle("grid_overlay")

                    elif self.btn_sound.collidepoint(mouse):
                        self._toggle("sound")

                    elif self.btn_color_r.collidepoint(mouse):
                        self._clamp_color(0, 20)

                    elif self.btn_color_g.collidepoint(mouse):
                        self._clamp_color(1, 20)

                    elif self.btn_color_b.collidepoint(mouse):
                        self._clamp_color(2, 20)

                    elif self.btn_color_rm.collidepoint(mouse):
                        self._clamp_color(0, -20)

                    elif self.btn_color_gm.collidepoint(mouse):
                        self._clamp_color(1, -20)

                    elif self.btn_color_bm.collidepoint(mouse):
                        self._clamp_color(2, -20)

                    elif self.btn_save.collidepoint(mouse):
                        save_settings(self.settings)  # сохраняем настройки в файл
                        return self.settings  # возвращаем новые настройки

            draw_background(self.surface)

            # заголовок SETTINGS
            draw_text(self.surface, "SETTINGS", self.font_title, CYAN,
                      WINDOW_WIDTH // 2, 40)

            # текст Grid overlay
            draw_text(self.surface, "Grid overlay:", self.font_md, WHITE,
                      200, 210, center=False)

            # ON/OFF для сетки
            grid_label = "ON" if self.settings["grid_overlay"] else "OFF"
            grid_col = GREEN if self.settings["grid_overlay"] else RED

            draw_button(self.surface, grid_label, self.font_btn, self.btn_grid,
                        hover=self.btn_grid.collidepoint(mouse))

            # текст Sound
            draw_text(self.surface, "Sound:", self.font_md, WHITE, 200, 270, center=False)

            # ON/OFF для звука
            snd_label = "ON" if self.settings["sound"] else "OFF"

            draw_button(self.surface, snd_label, self.font_btn, self.btn_sound,
                        hover=self.btn_sound.collidepoint(mouse))

            # эти строки просто убирают предупреждение, что переменные не используются
            _ = grid_col
            _ = snd_label

            # текст Snake color
            draw_text(self.surface, "Snake color:", self.font_md, WHITE, 30, 315, center=False)

            # прямоугольник предпросмотра цвета змейки
            preview_rect = pygame.Rect(490, 350, 60, 60)

            pygame.draw.rect(self.surface, tuple(self.settings["snake_color"]), preview_rect,
                             border_radius=6)

            pygame.draw.rect(self.surface, WHITE, preview_rect, 2, border_radius=6)

            # кнопки изменения RGB
            for btn, label in [
                (self.btn_color_r, "R+"), (self.btn_color_g, "G+"), (self.btn_color_b, "B+"),
                (self.btn_color_rm, "R-"), (self.btn_color_gm, "G-"), (self.btn_color_bm, "B-"),
            ]:
                draw_button(self.surface, label, self.font_btn, btn,
                            hover=btn.collidepoint(mouse))

            # кнопка сохранения
            draw_button(self.surface, "SAVE & BACK", self.font_btn, self.btn_save,
                        hover=self.btn_save.collidepoint(mouse))

            pygame.display.flip()


def main():
    pygame.init()  # запускаем pygame

    # создаем окно игры
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # название окна
    pygame.display.set_caption("Snake")

    # clock нужен для FPS
    clock = pygame.time.Clock()

    # загружаем настройки
    settings = load_settings()

    username = ""  # имя игрока
    player_id = None  # id игрока из базы
    personal_best = 0  # лучший результат

    # главный цикл всей программы
    while True:
        # запускаем главное меню
        menu = MainMenu(surface, clock, settings)
        action, username = menu.run()

        # если база работает и username есть — получаем игрока из базы
        if DB_AVAILABLE and username:
            try:
                player_id = db.get_or_create_player(username)
                personal_best = db.get_personal_best(player_id)
            except Exception:
                player_id = None
                personal_best = 0

        # если выбрали leaderboard
        if action == "leaderboard":
            LeaderboardScreen(surface, clock).run()
            continue

        # если выбрали settings
        if action == "settings":
            settings = SettingsScreen(surface, clock, settings).run()
            continue

        # игровой цикл
        while True:
            # создаем новую игру
            game = Game(settings, player_id, personal_best)
            running = True

            while running:
                dt = clock.tick(FPS)

                # обработка событий
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # ESC выходит из игры
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False

                    # передаем события в game.py
                    game.handle_event(event)

                # обновляем логику игры
                game.update(dt)

                # рисуем игру
                game.draw(surface)

                # обновляем экран
                pygame.display.flip()

                # если игра закончилась
                if game.over:

                    # сохраняем результат в базу, если база работает
                    if DB_AVAILABLE and player_id is not None:
                        try:
                            db.save_session(player_id, game.score, game.level)
                            personal_best = db.get_personal_best(player_id)
                            print(f"Saved: score={game.score} level={game.level}")
                        except Exception as e:
                            print(f"Save error: {e}")

                    else:
                        print(f"Not saved: DB_AVAILABLE={DB_AVAILABLE}, player_id={player_id}")

                    # показываем экран Game Over
                    screen = GameOverScreen(surface, clock, game.score,
                                            game.level, personal_best)

                    result = screen.run()

                    # если нажали retry — начинаем игру заново
                    if result == "retry":
                        break

                    # иначе возвращаемся в меню
                    else:
                        running = False
                        break

            # если игра не закончилась или выбрали menu — выходим в главное меню
            if not game.over or result == "menu":
                break


# запуск программы
if __name__ == "__main__":
    main()