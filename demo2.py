import pygame
import sys

pygame.init()

WIDTH = 1080
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HER ER CAPTION")

# CLOCK
clock = pygame.time.Clock()
FPS = 60

# PLAYER
x = 100
y = 100
speed = 5
size = 50

running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # wasd
    if keys[pygame.K_w]:
        y -= speed
    if keys[pygame.K_s]:
        y += speed
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed
         
    # DRAWING
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, size, size))

    pygame.display.flip()

pygame.quit()
sys.exit()