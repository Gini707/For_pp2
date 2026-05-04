import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Music player Pygame")

font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 26)

base = os.path.dirname(__file__)

playlist = [
    os.path.join(base, "music", "sample_tracks", "song1.mp3"),
    os.path.join(base, "music", "sample_tracks", "song2.mp3"),
    os.path.join(base, "music", "sample_tracks", "song3.mp3")
]

current_track = 0
running = True
is_playing = False

clock = pygame.time.Clock()


def format_time(seconds):
    seconds = max(0, int(seconds))
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes:02}:{sec:02}"


while running:
    screen.fill((255, 255, 255))

    text = font.render(
        "P = Play | S = Stop | N = Next track | B = Previous (Back) | Q = Quit",
        True,
        (0, 0, 0)
    )
    screen.blit(text, (70, 200))

    # current track information
    track_name = os.path.basename(playlist[current_track])
    track_text = font.render(f"Current track: {track_name}", True, (0, 0, 0))
    screen.blit(track_text, (240, 270))

    # playback progress / track position
    position_ms = pygame.mixer.music.get_pos()
    if position_ms == -1:
        position_sec = 0
    else:
        position_sec = position_ms / 1000

    progress_text = small_font.render(
        f"Position: {format_time(position_sec)}",
        True,
        (0, 0, 0)
    )
    screen.blit(progress_text, (330, 320))

    # simple progress bar
    bar_x = 200
    bar_y = 370
    bar_width = 400
    bar_height = 20

    pygame.draw.rect(screen, (180, 180, 180), (bar_x, bar_y, bar_width, bar_height))

    # условно считаем длину трека 180 секунд
    track_length = 180
    filled_width = int((position_sec / track_length) * bar_width)
    if filled_width > bar_width:
        filled_width = bar_width

    pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, filled_width, bar_height))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            elif event.key == pygame.K_p:
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
                is_playing = True

            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                is_playing = False

            elif event.key == pygame.K_n:
                current_track += 1
                if current_track >= len(playlist):
                    current_track = 0
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
                is_playing = True

            elif event.key == pygame.K_b:
                current_track -= 1
                if current_track < 0:
                    current_track = len(playlist) - 1
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
                is_playing = True

    clock.tick(60)

pygame.quit()