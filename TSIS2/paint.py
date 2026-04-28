import pygame
import datetime
from tools import draw_pencil, draw_line, draw_rect, draw_circle, flood_fill

pygame.init()  # инициализация pygame

# размеры окна
WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90  # высота панели инструментов

# создаём окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extended Paint")

clock = pygame.time.Clock()

# 🎯 ОСНОВНОЙ ХОЛСТ ДЛЯ РИСОВАНИЯ
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))  # белый фон

# шрифты
font = pygame.font.SysFont("Arial", 22)
text_font = pygame.font.SysFont("Arial", 32)

# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (210, 210, 210)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

colors = [BLACK, RED, GREEN, BLUE, YELLOW]

# текущие настройки
current_color = BLACK
brush_size = 5
tool = "pencil"

# состояния рисования
drawing = False
start_pos = None
last_pos = None

# текстовый режим
text_mode = False
text_position = None
text_value = ""


# 🎯 ОТРИСОВКА ПАНЕЛИ ИНСТРУМЕНТОВ
def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    info = f"Tool: {tool} | Brush: {brush_size}px"
    screen.blit(font.render(info, True, BLACK), (20, 10))

    # подсказки клавиш
    help_text = "P Pencil | L Line | R Rect | C Circle | F Fill | T Text | 1/2/3 Size | Ctrl+S Save"
    screen.blit(font.render(help_text, True, BLACK), (20, 40))

    # выбор цвета
    x = 720
    for color in colors:
        pygame.draw.rect(screen, color, (x, 25, 40, 40))
        pygame.draw.rect(screen, BLACK, (x, 25, 40, 40), 2)
        x += 50


# 🎯 перевод координат мыши в координаты canvas
def canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR_HEIGHT


# 🎯 СОХРАНЕНИЕ В PNG
def save_canvas():
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"paint_save_{now}.png"
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


running = True

while running:
    screen.fill(WHITE)

    # отображаем canvas
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    mouse_pos = pygame.mouse.get_pos()
    canvas_mouse = canvas_pos(mouse_pos)

    for event in pygame.event.get():

        # ❌ выход из программы
        if event.type == pygame.QUIT:
            running = False

        # ⌨️ КЛАВИАТУРА
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            # 💾 Ctrl+S — сохранение
            if keys[pygame.K_LCTRL] and event.key == pygame.K_s:
                save_canvas()

            # 🎨 размер кисти
            elif event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            # 🔤 РЕЖИМ ТЕКСТА
            elif text_mode:
                if event.key == pygame.K_RETURN:
                    # текст сохраняется на canvas
                    rendered_text = text_font.render(text_value, True, current_color)
                    canvas.blit(rendered_text, text_position)
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    # отмена текста
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                # 🔧 выбор инструмента
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_t:
                    tool = "text"

        # 🖱 НАЖАТИЕ МЫШИ
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = mouse_pos

                # 🎨 выбор цвета
                if y < TOOLBAR_HEIGHT:
                    color_x = 720
                    for color in colors:
                        rect = pygame.Rect(color_x, 25, 40, 40)
                        if rect.collidepoint(mouse_pos):
                            current_color = color
                        color_x += 50

                else:
                    cx, cy = canvas_mouse

                    # ✏️ карандаш
                    if tool == "pencil":
                        drawing = True
                        last_pos = (cx, cy)

                    # 📏 фигуры
                    elif tool in ["line", "rect", "circle"]:
                        drawing = True
                        start_pos = (cx, cy)

                    # 🎨 заливка
                    elif tool == "fill":
                        flood_fill(canvas, cx, cy, current_color)

                    # 🔤 текст
                    elif tool == "text":
                        text_mode = True
                        text_position = (cx, cy)
                        text_value = ""

        # 🖱 ОТПУСКАНИЕ МЫШИ
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                cx, cy = canvas_mouse
                end_pos = (cx, cy)

                # 📏 финальное рисование фигуры
                if tool == "line":
                    draw_line(canvas, current_color, start_pos, end_pos, brush_size)

                elif tool == "rect":
                    draw_rect(canvas, current_color, start_pos, end_pos, brush_size)

                elif tool == "circle":
                    draw_circle(canvas, current_color, start_pos, end_pos, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

        # 🖱 ДВИЖЕНИЕ МЫШИ — САМОЕ ВАЖНОЕ (рисование)
        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pencil":
                cx, cy = canvas_mouse
                current_pos = (cx, cy)

                # ✏️ рисуем линию между точками → freehand drawing
                draw_pencil(canvas, current_color, last_pos, current_pos, brush_size)

                last_pos = current_pos

    # 👁 PREVIEW (временная фигура)
    if drawing and tool in ["line", "rect", "circle"] and start_pos:
        preview = canvas.copy()  # копия холста

        cx, cy = canvas_mouse
        end_pos = (cx, cy)

        if tool == "line":
            draw_line(preview, current_color, start_pos, end_pos, brush_size)

        elif tool == "rect":
            draw_rect(preview, current_color, start_pos, end_pos, brush_size)

        elif tool == "circle":
            draw_circle(preview, current_color, start_pos, end_pos, brush_size)

        # показываем preview (не сохраняем)
        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    # 🔤 отображение текста в процессе набора
    if text_mode:
        rendered_text = text_font.render(text_value, True, current_color)
        screen.blit(rendered_text, (text_position[0], text_position[1] + TOOLBAR_HEIGHT))

    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()