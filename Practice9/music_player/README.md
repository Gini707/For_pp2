Music Player with Keyboard Controller

This program is a simple music player made with pygame.

## Features
- Play track with P
- Stop track with S
- Next track with N
- Previous track with B
- Quit with Q
- Display current track name
- Display track position in seconds

## Music folder
Put your audio files into:
music/sample_tracks/

## Run
```bash
python main.py

---

# 5. Задача 3 — Mickey Clock

Тут дам код так, чтобы он работал даже если у тебя только **одна картинка руки** `mickey_hand.png`.

---

## Файл: `Practice9/mickey_clock/clock.py`

```python
import os
from datetime import datetime
import pygame


def load_hand_image():
    image_path = os.path.join("images", "mickey_hand.png")
    image = pygame.image.load(image_path).convert_alpha()
    return image


def get_time_angles():
    now = datetime.now()
    minutes = now.minute
    seconds = now.second

    minute_angle = -minutes * 6
    second_angle = -seconds * 6

    return minute_angle, second_angle, minutes, seconds


def rotate_hand(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=center)
    return rotated_image, rotated_rect


def scale_hand(image, width, height):
    return pygame.transform.smoothscale(image, (width, height))
Файл: Practice9/mickey_clock/main.py
import pygame
from clock import load_hand_image, get_time_angles, rotate_hand, scale_hand


WIDTH = 800
HEIGHT = 600
FPS = 60


def draw_text(screen, text, font, x, y, color=(0, 0, 0)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock Application")
    game_clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    center = (WIDTH // 2, HEIGHT // 2)

    original_hand = load_hand_image()

    minute_hand = scale_hand(original_hand, 40, 180)
    second_hand = scale_hand(original_hand, 25, 220)

    running = True
    while running:
        game_clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        minute_angle, second_angle, minutes, seconds = get_time_angles()

        screen.fill((240, 240, 240))

        pygame.draw.circle(screen, (220, 220, 220), center, 220)
        pygame.draw.circle(screen, (0, 0, 0), center, 220, 3)
        pygame.draw.circle(screen, (0, 0, 0), center, 8)

        for i in range(60):
            angle = i * 6
            vector = pygame.math.Vector2(0, -1).rotate(angle)

            start_pos = (
                center[0] + vector.x * 190,
                center[1] + vector.y * 190
            )
            end_pos = (
                center[0] + vector.x * 210,
                center[1] + vector.y * 210
            )

            width = 3 if i % 5 == 0 else 1
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, width)

        rotated_minute, minute_rect = rotate_hand(minute_hand, minute_angle, center)
        rotated_second, second_rect = rotate_hand(second_hand, second_angle, center)

        screen.blit(rotated_minute, minute_rect)
        screen.blit(rotated_second, second_rect)

        time_text = f"{minutes:02}:{seconds:02}"
        draw_text(screen, time_text, font, 350, 40)
        draw_text(screen, "Right hand = minutes | Left hand = seconds", small_font, 220, 540)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
Файл: Practice9/mickey_clock/README.md
# Mickey's Clock Application

This program displays the current system time using Mickey Mouse hand graphics.

## Features
- Shows minutes and seconds
- Updates every second
- Uses rotated hand images
- Synchronized with system time

## Notes
- Right hand = minute hand
- Left hand = second hand
- Uses pygame.transform.rotate()

## Run
```bash
python main.py

---

# 6. Главный `README.md`

Файл: **Practice9/README.md**

```md
# Practice9 - Pygame Tasks

This project contains 3 pygame programs:

1. Mickey's Clock Application
2. Music Player with Keyboard Controller
3. Moving Ball Game

## Requirements
- Python 3.x
- pygame>=2.0.0

## Install
```bash
pip install -r requirements.txt
Run programs
Moving Ball
cd moving_ball
python main.py
Music Player
cd music_player
python main.py
Mickey Clock
cd mickey_clock
python main.py

---

# 7. Куда какой код вставить

## `moving_ball`
- `ball.py` → код с классом Ball
- `main.py` → код запуска moving ball
- `README.md` → текст для moving ball

## `music_player`
- `player.py` → код с классом MusicPlayer
- `main.py` → код запуска music player
- `README.md` → текст для music player

## `mickey_clock`
- `clock.py` → код с функциями часов
- `main.py` → код запуска часов
- `README.md` → текст для часов

## корень `Practice9`
- `requirements.txt` → `pygame>=2.0.0`
- `README.md` → общий текст

---

# 8. Как запускать

## Moving Ball
Открой терминал:

```bash
cd Practice9/moving_ball
python main.py
Music Player
cd Practice9/music_player
python main.py
Mickey Clock
cd Practice9/mickey_clock
python main.py
9. Если будет ошибка с путями

Запускай из папки конкретной задачи.

Например для music player:

cd C:\Users\Lenovo\Desktop\pp2 hw\Practice9\music_player
python main.py

Для mickey clock:

cd C:\Users\Lenovo\Desktop\pp2 hw\Practice9\mickey_clock
python main.py
10. Очень важный момент про mickey_hand.png

Файл должен лежать именно тут:

Practice9/mickey_clock/images/mickey_hand.png

И название должно быть точно:

mickey_hand.png
11. Если хочешь сдать красиво

После того как всё вставишь, в терминале в папке Practice9:

git add .
git commit -m "Add Practice9 - Pygame tasks"
git push origin main
12. Самое главное

Сначала проверь по отдельности:

moving_ball
music_player
mickey_clock

Если одна задача не запускается, не запускай всё сразу — проверяй именно её папку.

Если хочешь, следующим сообщением я могу дать тебе ещё и очень простое объяснение каждой строчки кода, чтобы ты смог рассказать преподавателю.