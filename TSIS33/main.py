import pygame
from racer import RacerGame, WIDTH, HEIGHT
from ui import Button, draw_text, draw_center_text, WHITE, BLACK, BLUE
from persistence import load_settings, save_settings, load_leaderboard


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Racer")

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)
clock = pygame.time.Clock()

settings = load_settings()


def ask_username():
    name = ""
    active = True

    while active:
        screen.fill((30, 30, 30))
        draw_center_text(screen, "Enter your name", big_font, WHITE, 180)
        draw_center_text(screen, name + "|", font, WHITE, 280)
        draw_center_text(screen, "Press Enter to start", font, WHITE, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        name = "Player"
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    play_btn = Button(300, 190, 200, 55, "Play")
    leaderboard_btn = Button(300, 260, 200, 55, "Leaderboard")
    settings_btn = Button(300, 330, 200, 55, "Settings")
    quit_btn = Button(300, 400, 200, 55, "Quit")

    while True:
        screen.fill((40, 120, 70))
        draw_center_text(screen, "ARCADE RACER", big_font, WHITE, 110)

        for btn in [play_btn, leaderboard_btn, settings_btn, quit_btn]:
            btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play_btn.clicked(event):
                return "play"

            if leaderboard_btn.clicked(event):
                return "leaderboard"

            if settings_btn.clicked(event):
                return "settings"

            if quit_btn.clicked(event):
                return "quit"

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    back_btn = Button(300, 520, 200, 50, "Back")
    scores = load_leaderboard()

    while True:
        screen.fill((25, 25, 25))
        draw_center_text(screen, "TOP 10 LEADERBOARD", big_font, WHITE, 70)

        y = 140

        if not scores:
            draw_center_text(screen, "No scores yet", font, WHITE, 250)
        else:
            for i, item in enumerate(scores[:10], start=1):
                line = f"{i}. {item['name']} | Score: {item['score']} | Distance: {item['distance']}m"
                draw_text(screen, line, font, WHITE, 180, y)
                y += 35

        back_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back_btn.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def settings_screen():
    global settings

    sound_btn = Button(260, 180, 280, 50, "")
    color_btn = Button(260, 250, 280, 50, "")
    difficulty_btn = Button(260, 320, 280, 50, "")
    back_btn = Button(300, 500, 200, 50, "Back")

    colors = ["red", "blue", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill((35, 35, 70))
        draw_center_text(screen, "SETTINGS", big_font, WHITE, 90)

        sound_btn.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_btn.text = f"Car Color: {settings['car_color']}"
        difficulty_btn.text = f"Difficulty: {settings['difficulty']}"

        for btn in [sound_btn, color_btn, difficulty_btn, back_btn]:
            btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if color_btn.clicked(event):
                index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(index + 1) % len(colors)]
                save_settings(settings)

            if difficulty_btn.clicked(event):
                index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                save_settings(settings)

            if back_btn.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(result):
    retry_btn = Button(260, 380, 280, 55, "Retry")
    menu_btn = Button(260, 450, 280, 55, "Main Menu")

    while True:
        screen.fill((80, 30, 30))
        draw_center_text(screen, "GAME OVER", big_font, WHITE, 120)

        draw_center_text(screen, f"Score: {result['score']}", font, WHITE, 210)
        draw_center_text(screen, f"Distance: {result['distance']} m", font, WHITE, 250)
        draw_center_text(screen, f"Coins: {result['coins']}", font, WHITE, 290)

        retry_btn.draw(screen, font)
        menu_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry_btn.clicked(event):
                return "retry"

            if menu_btn.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def main():
    while True:
        action = main_menu()

        if action == "quit":
            break

        elif action == "leaderboard":
            result = leaderboard_screen()
            if result == "quit":
                break

        elif action == "settings":
            result = settings_screen()
            if result == "quit":
                break

        elif action == "play":
            username = ask_username()

            if username is None:
                break

            while True:
                current_settings = load_settings()
                game = RacerGame(screen, username, current_settings)
                result = game.run()

                if result == "quit":
                    pygame.quit()
                    return

                over_action = game_over_screen(result)

                if over_action == "quit":
                    pygame.quit()
                    return

                elif over_action == "menu":
                    break

                elif over_action == "retry":
                    continue

    pygame.quit()


main()