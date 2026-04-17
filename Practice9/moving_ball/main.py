import pygame 
pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Game")    
clock = pygame.time.Clock()

running = True

x = 400
y = 300

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x - 20 >= 25: x -= 20
            elif event.key == pygame.K_RIGHT:
                if x + 20 <= 800 - 25: x += 20
            elif event.key == pygame.K_UP:
                if y - 20 >= 25: y -= 20
            elif event.key == pygame.K_DOWN:
               if y + 20 <= 600 - 25: y += 20
    screen.fill('WHITE')
    pygame.draw.circle(screen, (255,0,0), (x, y), 25)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
    
            
        