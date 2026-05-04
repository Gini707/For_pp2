import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)

# --- generate food with weight ---
def generate_food():
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        
        if (x, y) not in snake:
            value = random.choice([1, 2, 3])  # вес еды
            return (x, y, value)

food = generate_food()
food_spawn_time = pygame.time.get_ticks()  # время появления еды
FOOD_LIFETIME = 5000  # 5 секунд

score = 0
level = 1
food_eaten = 0
speed = 10

running = True
while running:
    screen.fill(BLACK)

    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # --- collision with walls ---
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT):
        running = False

    # --- collision with itself ---
    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    fx, fy, food_value = food

    # --- eating food ---
    if new_head == (fx, fy):
        score += food_value  # добавляем вес еды
        food_eaten += 1
        food = generate_food()
        food_spawn_time = pygame.time.get_ticks()  # обновляем таймер
    else:
        snake.pop()

    # --- food disappears after time ---
    if current_time - food_spawn_time > FOOD_LIFETIME:
        food = generate_food()
        food_spawn_time = pygame.time.get_ticks()

    # --- level system ---
    if food_eaten >= 3:
        level += 1
        food_eaten = 0
        speed += 2  

    # --- draw snake ---
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # --- draw food with different colors ---
    if food_value == 1:
        color = RED
    elif food_value == 2:
        color = YELLOW
    else:
        color = WHITE

    pygame.draw.rect(screen, color, (fx, fy, CELL_SIZE, CELL_SIZE))

    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()