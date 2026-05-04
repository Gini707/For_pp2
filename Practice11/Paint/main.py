import pygame
import math
pygame.init()

Width = 1000
Height = 800

screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

color = Black

# --- выбор цвета ---
keys = {
    pygame.K_0: White,
    pygame.K_1: Black,
    pygame.K_2: Red,
    pygame.K_3: Green,
    pygame.K_4: Blue,
}

mode = "draw"
start_pos = None
drawing = False
last_pos = None

# --- основной холст ---
canvas = pygame.Surface((Width, Height))
canvas.fill(White)

# --- слой для превью ---
preview = pygame.Surface((Width, Height), pygame.SRCALPHA)

running = True

while running:

    preview.fill((0, 0, 0, 0))  # очищаем превью каждый кадр

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- выбор режима ---
        if event.type == pygame.KEYDOWN:
            if event.key in keys:
                color = keys[event.key]

            if event.key == pygame.K_d:
                mode = "draw"
            if event.key == pygame.K_e:
                mode = "eraser"
            if event.key == pygame.K_r:
                mode = "rect"
            if event.key == pygame.K_o:
                mode = "circle"
            if event.key == pygame.K_s:
                mode = "square"      # квадрат
            if event.key == pygame.K_t:
                mode = "triangle"    # прямоугольный треугольник
            if event.key == pygame.K_y:
                mode = "eq_triangle" # равносторонний
            if event.key == pygame.K_h:
                mode = "rhombus"     # ромб

            if event.key == pygame.K_c:
                canvas.fill(White)

        # --- начало рисования ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = pygame.mouse.get_pos()
            last_pos = start_pos

        # --- конец рисования ---
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = pygame.mouse.get_pos()

            if start_pos:

                x1, y1 = start_pos
                x2, y2 = end_pos

                # --- RECT ---
                if mode == "rect":
                    rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
                    pygame.draw.rect(canvas, color, rect, 2)

                # --- CIRCLE ---
                if mode == "circle":
                    rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
                    pygame.draw.ellipse(canvas, color, rect, 2)

                # --- SQUARE ---
                if mode == "square":
                    size = min(abs(x2-x1), abs(y2-y1))
                    rect = pygame.Rect(x1, y1, size, size)
                    pygame.draw.rect(canvas, color, rect, 2)

                # --- RIGHT TRIANGLE ---
                if mode == "triangle":
                    points = [(x1,y1), (x2,y2), (x1,y2)]
                    pygame.draw.polygon(canvas, color, points, 2)

                # --- EQUILATERAL TRIANGLE ---
                if mode == "eq_triangle":
                    side = abs(x2 - x1)
                    height = side * math.sqrt(3) / 2
                    points = [
                        (x1, y2),
                        (x1 + side, y2),
                        (x1 + side/2, y2 - height)
                    ]
                    pygame.draw.polygon(canvas, color, points, 2)

                # --- RHOMBUS ---
                if mode == "rhombus":
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2

                    points = [
                        (cx, cy - dy),
                        (cx + dx, cy),
                        (cx, cy + dy),
                        (cx - dx, cy)
                    ]
                    pygame.draw.polygon(canvas, color, points, 2)

            start_pos = None
            last_pos = None

    x, y = pygame.mouse.get_pos()

    # --- DRAW / ERASER ---
    if drawing and mode in ["draw", "eraser"]:
        draw_color = White if mode == "eraser" else color
        if last_pos:
            pygame.draw.line(canvas, draw_color, last_pos, (x, y), 10)
        last_pos = (x, y)

    # --- PREVIEW RECT ---
    if drawing and start_pos:
        x1, y1 = start_pos

        if mode == "rect":
            rect = pygame.Rect(min(x1,x), min(y1,y), abs(x-x1), abs(y-y1))
            pygame.draw.rect(preview, color, rect, 2)

        if mode == "circle":
            rect = pygame.Rect(min(x1,x), min(y1,y), abs(x-x1), abs(y-y1))
            pygame.draw.ellipse(preview, color, rect, 2)

        if mode == "square":
            size = min(abs(x-x1), abs(y-y1))
            rect = pygame.Rect(x1, y1, size, size)
            pygame.draw.rect(preview, color, rect, 2)

        if mode == "triangle":
            pygame.draw.polygon(preview, color, [(x1,y1), (x,y), (x1,y)], 2)

        if mode == "eq_triangle":
            side = abs(x - x1)
            height = side * math.sqrt(3) / 2
            points = [(x1,y), (x1+side,y), (x1+side/2, y-height)]
            pygame.draw.polygon(preview, color, points, 2)

        if mode == "rhombus":
            cx = (x1 + x)//2
            cy = (y1 + y)//2
            dx = abs(x - x1)//2
            dy = abs(y - y1)//2

            points = [(cx,cy-dy),(cx+dx,cy),(cx,cy+dy),(cx-dx,cy)]
            pygame.draw.polygon(preview, color, points, 2)

    # --- вывод ---
    screen.blit(canvas, (0, 0))
    screen.blit(preview, (0, 0))

    pygame.display.flip()
    clock.tick(144)