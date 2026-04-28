import pygame          # Импортируем библиотеку pygame для создания игры
import sys             # Нужен для полного выхода из программы

# Импортируем главный игровой класс GameSession из файла racer.py
from racer import GameSession

# Импортируем все экраны и цвета из файла ui.py
from ui import (
    main_menu,
    settings_screen,
    username_screen,
    game_over_screen,
    leaderboard_screen,
    draw_hud,
    draw_background,
    DARK,
    PINK,
    WHITE
)

# Импортируем функции для сохранения и загрузки настроек и leaderboard
from persistence import (
    load_settings,
    save_settings,
    load_leaderboard,
    save_score
)


# Размер окна игры
W, H = 480, 720

# FPS — сколько кадров в секунду будет обновляться игра
FPS = 60


# Состояния игры
STATE_MENU = "menu"                 # Главное меню
STATE_USERNAME = "username"         # Экран ввода имени
STATE_GAME = "game"                 # Сам игровой процесс
STATE_GAMEOVER = "gameover"         # Экран после проигрыша
STATE_LEADERBOARD = "leaderboard"   # Таблица лидеров
STATE_SETTINGS = "settings"         # Настройки


# Функция включает или выключает музыку
def apply_music(sound_on):
    if sound_on:
        pygame.mixer.music.unpause()   # Если звук включен — продолжаем музыку
    else:
        pygame.mixer.music.pause()     # Если звук выключен — ставим музыку на паузу


def main():
    # Запускаем pygame
    pygame.init()

    # Запускаем модуль музыки и звуков
    pygame.mixer.init()

    # Создаем окно игры размером 480x720
    screen = pygame.display.set_mode((W, H))

    # Название окна
    pygame.display.set_caption("Racer ♥")

    # Clock нужен, чтобы контролировать FPS
    clock = pygame.time.Clock()

    # Загружаем настройки из файла settings.json
    settings = load_settings()

    # Загружаем таблицу лидеров из файла leaderboard.json
    leaderboard = load_leaderboard()

    # Пробуем загрузить и включить музыку
    try:
        pygame.mixer.music.load("assets/music.mp3")  # Загружаем музыку
        pygame.mixer.music.set_volume(0.5)           # Ставим громкость 50%
        pygame.mixer.music.play(-1)                  # -1 значит музыка играет бесконечно

        # Если в настройках звук выключен, сразу ставим музыку на паузу
        if not settings["sound"]:
            pygame.mixer.music.pause()

    except Exception:
        # Если файл музыки не найден или ошибка — игра все равно продолжит работать
        pass

    # Начальное состояние игры — главное меню
    state = STATE_MENU

    # Имя игрока
    username = ""

    # Временный текст, который игрок вводит на экране username
    username_buf = ""

    # Здесь будет объект игровой сессии GameSession
    session = None

    # Переменная для анимации фона/меню
    menu_scroll = 0

    # Финальные результаты после проигрыша
    final_score = final_dist = final_coins = 0

    # Главный бесконечный цикл игры
    while True:
        # dt — время между кадрами в секундах
        # Нужно для плавного движения объектов
        dt = clock.tick(FPS) / 1000.0

        # Получаем позицию мышки
        mouse_pos = pygame.mouse.get_pos()

        # Обновляем значение прокрутки меню
        menu_scroll = (menu_scroll + 1) % 10000

        # Обрабатываем все события pygame
        for event in pygame.event.get():

            # Если пользователь нажал крестик окна
            if event.type == pygame.QUIT:
                save_settings(settings)  # Сохраняем настройки
                pygame.quit()            # Закрываем pygame
                sys.exit()               # Полностью закрываем программу

            # =========================
            # СОСТОЯНИЕ: ГЛАВНОЕ МЕНЮ
            # =========================
            if state == STATE_MENU:

                # Если нажали мышкой
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Получаем кнопки главного меню
                    btns = main_menu(screen, W, H, mouse_pos, menu_scroll)

                    # Проверяем, на какую кнопку нажали
                    for i, r in enumerate(btns):

                        # Если мышка попала внутрь кнопки
                        if r.collidepoint(mouse_pos):

                            if i == 0:
                                # Первая кнопка — начать игру
                                state = STATE_USERNAME
                                username_buf = ""

                            elif i == 1:
                                # Вторая кнопка — leaderboard
                                leaderboard = load_leaderboard()
                                state = STATE_LEADERBOARD

                            elif i == 2:
                                # Третья кнопка — настройки
                                state = STATE_SETTINGS

                            elif i == 3:
                                # Четвертая кнопка — выход
                                save_settings(settings)
                                pygame.quit()
                                sys.exit()

            # =========================
            # СОСТОЯНИЕ: ВВОД ИМЕНИ
            # =========================
            elif state == STATE_USERNAME:

                # Если нажали клавишу
                if event.type == pygame.KEYDOWN:

                    # Enter запускает игру, если имя не пустое
                    if event.key == pygame.K_RETURN and username_buf.strip():
                        username = username_buf.strip()

                        # Создаем новую игровую сессию
                        # Передаем цвет машины и сложность из настроек
                        session = GameSession(
                            W,
                            H,
                            settings["car_color"],
                            settings["difficulty"]
                        )

                        # Переходим в игру
                        state = STATE_GAME

                    # Backspace удаляет последний символ
                    elif event.key == pygame.K_BACKSPACE:
                        username_buf = username_buf[:-1]

                    # Escape возвращает в главное меню
                    elif event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

                    else:
                        # Добавляем символ в имя, если длина меньше 16
                        if len(username_buf) < 16 and event.unicode.isprintable():
                            username_buf += event.unicode

            # =========================
            # СОСТОЯНИЕ: ИГРА
            # =========================
            elif state == STATE_GAME:

                # Если нажали клавишу
                if event.type == pygame.KEYDOWN:

                    # Escape возвращает в меню
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

                    else:
                        # Остальные клавиши передаются в GameSession
                        # Например, движение машины или использование действий
                        session.on_key_down(event.key)

            # =========================
            # СОСТОЯНИЕ: GAME OVER
            # =========================
            elif state == STATE_GAMEOVER:

                # Если нажали мышкой
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Получаем кнопки экрана Game Over
                    btns = game_over_screen(
                        screen,
                        W,
                        H,
                        mouse_pos,
                        final_score,
                        final_dist,
                        final_coins,
                        menu_scroll
                    )

                    # Проверяем кнопки
                    for i, r in enumerate(btns):

                        if r.collidepoint(mouse_pos):

                            if i == 0:
                                # Первая кнопка — играть заново
                                session = GameSession(
                                    W,
                                    H,
                                    settings["car_color"],
                                    settings["difficulty"]
                                )

                                state = STATE_GAME

                            elif i == 1:
                                # Вторая кнопка — назад в меню
                                state = STATE_MENU

            # =========================
            # СОСТОЯНИЕ: LEADERBOARD
            # =========================
            elif state == STATE_LEADERBOARD:

                # Если нажали мышкой
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Получаем кнопку назад
                    btns = leaderboard_screen(
                        screen,
                        W,
                        H,
                        mouse_pos,
                        leaderboard,
                        menu_scroll
                    )

                    # Если нажали Back — возвращаемся в меню
                    if btns[0].collidepoint(mouse_pos):
                        state = STATE_MENU

            # =========================
            # СОСТОЯНИЕ: SETTINGS
            # =========================
            elif state == STATE_SETTINGS:

                # Если нажали мышкой
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Получаем элементы настроек
                    items = settings_screen(
                        screen,
                        W,
                        H,
                        mouse_pos,
                        settings,
                        menu_scroll
                    )

                    # Проверяем каждый элемент настроек
                    for tag, item in items:

                        # Настройка звука
                        if tag == "sound" and item.collidepoint(mouse_pos):
                            settings["sound"] = not settings["sound"]
                            save_settings(settings)
                            apply_music(settings["sound"])

                        # Выбор цвета машины
                        elif tag == "color_row":
                            for name, cr in item.items():

                                # Если нажали на цвет
                                if cr.collidepoint(mouse_pos):
                                    settings["car_color"] = name
                                    save_settings(settings)

                        # Выбор сложности
                        elif tag == "diff_row":
                            for d, dr in item.items():

                                # Если нажали на сложность
                                if dr.collidepoint(mouse_pos):
                                    settings["difficulty"] = d
                                    save_settings(settings)

                        # Кнопка назад
                        elif tag == "back" and item.collidepoint(mouse_pos):
                            state = STATE_MENU

        # =========================
        # ОБНОВЛЕНИЕ ИГРЫ
        # =========================

        # Если мы в игре и session существует
        if state == STATE_GAME and session:

            # Обновляем всю игровую логику:
            # движение машины, врагов, монет, препятствий, power-ups
            session.update(dt)

            # Если игрок проиграл
            if not session.alive:

                # Сохраняем финальные результаты
                final_score = session.score
                final_dist = session.distance
                final_coins = session.coins

                # Сохраняем результат игрока в leaderboard
                leaderboard = save_score(
                    username,
                    final_score,
                    final_dist,
                    final_coins
                )

                # Переходим на экран Game Over
                state = STATE_GAMEOVER

        # Заливаем экран темным цветом
        screen.fill(DARK)

        # =========================
        # ОТРИСОВКА ЭКРАНОВ
        # =========================

        if state == STATE_MENU:
            # Рисуем главное меню
            main_menu(screen, W, H, mouse_pos, menu_scroll)

        elif state == STATE_USERNAME:
            # Рисуем экран ввода имени
            username_screen(screen, W, H, username_buf, menu_scroll)

        elif state == STATE_GAME and session:
            # Рисуем саму игру
            session.draw(screen)

            # Рисуем HUD сверху:
            # score, distance, coins, power-up, shield
            draw_hud(
                screen,
                W,
                session.score,
                session.distance,
                session.coins,
                session.active_powerup,
                session.powerup_timer,
                session.shield_active,
                0
            )

        elif state == STATE_GAMEOVER:
            # Рисуем экран проигрыша
            game_over_screen(
                screen,
                W,
                H,
                mouse_pos,
                final_score,
                final_dist,
                final_coins,
                menu_scroll
            )

        elif state == STATE_LEADERBOARD:
            # Рисуем таблицу лидеров
            leaderboard_screen(
                screen,
                W,
                H,
                mouse_pos,
                leaderboard,
                menu_scroll
            )

        elif state == STATE_SETTINGS:
            # Рисуем экран настроек
            settings_screen(
                screen,
                W,
                H,
                mouse_pos,
                settings,
                menu_scroll
            )

        # Обновляем экран
        pygame.display.flip()


# Эта часть запускает main(), только если файл запущен напрямую
if __name__ == "__main__":
    main()