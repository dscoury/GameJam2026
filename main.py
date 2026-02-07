import pygame
import random
import sys

# SETUP

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sumo Growth DDR")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
legend_font = pygame.font.SysFont(None, 24)

# CONSTANTS

FPS = 60
GAME_LENGTH = 45 * FPS # 45 sekunder

TIMING_Y = 420
TIMING_HEIGHT = 24

LANES = {
    1: 200, # Player 1 lane (WASD)
    2: 550, # Player 2 lane (Piltaster)
}

FOOD_COLORS = {
    "good": (80, 220, 120),     # green
    "bad": (220, 80, 80),       # red
    "raw": (200, 200, 200)      # gray
}

MISS_PENALTY = {
    "good": 4,
    "bad": 2,
    "raw": 1
}

# PLAYER DATA

p1_size = 50
p2_size = 50

p1_rect = pygame.Rect(LANES[1] - 25, 470, 50, 50)
p2_rect = pygame.Rect(LANES[2] - 25, 470, 50, 50)

# FOOD

foods = []
spawn_timer = 0
spawn_delay = 60
food_speed = 4

def spawn_food():
    lane = random.choice([1, 2])
    food_type = random.choice(["good", "bad", "raw"])
    rect = pygame.Rect(LANES[lane] - 15, -30, 30, 30)
    foods.append({
        "rect": rect,
        "type": food_type,
        "lane": lane
    })

# GAME STATE

timer = GAME_LENGTH
running = True
game_over = False

while running:
    clock.tick(FPS)
    screen.fill((25, 25, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            spawn_food()
            spawn_timer = 0


    for food in foods[:]:
        food["rect"].y += food_speed

        in_zone = (
            TIMING_Y <= food["rect"].y <= TIMING_Y + TIMING_HEIGHT
        )

        if in_zone and food["lane"] == 1:
            if food["type"] == "good" and keys[pygame.K_w]:
                p1_size += 5
                foods.remove(food)

            elif food["type"] == "bad" and keys[pygame.K_d]:
                foods.remove(food)

            elif food["type"] == "raw" and keys[pygame.K_a]:
                foods.remove(food)

        if in_zone and food["lane"] == 2:
            if food["type"] == "good" and keys[pygame.K_UP]:
                p2_size += 5
                foods.remove(food)

            elif food["type"] == "bad" and keys[pygame.K_RIGHT]:
                foods.remove(food)

            elif food["type"] == "raw" and keys[pygame.K_LEFT]:
                foods.remove(food)

        if food in foods and food["rect"].y > TIMING_Y + TIMING_HEIGHT + 30:
            penalty = MISS_PENALTY[food["type"]]

            if food["lane"] == 1:
                p1_size -= penalty
            else:
                p2_size -= penalty

            foods.remove(food)
    
    p1_size = max(30, p1_size)
    p2_size = max(30, p2_size)

    p1_rect.width = p1_size
    p1_rect.height = p1_size
    p1_rect.centerx = LANES[1]
    p1_rect.bottom = HEIGHT - 40

    p2_rect.width = p2_size
    p2_rect.height = p2_size
    p2_rect.centerx = LANES[2]
    p2_rect.bottom = HEIGHT - 40

    pygame.draw.rect(
        screen,
        (200, 200, 0),
        (0, TIMING_Y, WIDTH, TIMING_HEIGHT)
    )

    pygame.draw.line(screen, (80, 80, 80), (400, 0), (400, HEIGHT), 2)

    pygame.draw.rect(screen, (200, 80, 80), p1_rect)
    pygame.draw.rect(screen, (80, 80, 220), p2_rect)

    for food in foods:
        pygame.draw.rect(
            screen,
            FOOD_COLORS[food["type"]],
            food["rect"]
        )

    legend_p1 = [
        "PLAYER 1 (RED) - WASD",
        "W : Eat good food",
        "D : Pass junk food",
        "A : Reject raw food"
    ]

    legend_p2 = [
        "PLAYER 2 (BLUE) - ARROWS",
        "UP    : Eat good food",
        "RIGHT : Pass junk food",
        "LEFT  : Reject raw food"
    ]

    for i, line in enumerate(legend_p1):
        screen.blit(
            legend_font.render(line, True, (220, 100, 100)),
            (20, 20 + i * 22)
        )

    for i, line in enumerate(legend_p2):
        text = legend_font.render(line, True, (100, 100, 220))
        screen.blit(
            text,
            (WIDTH - text.get_width() - 20, 20 + i * 22)
        )

    food_legend_y = 120
    screen.blit(legend_font.render("FOOD TYPES:", True, (255, 255, 255)),
                (WIDTH // 2 - 60, food_legend_y))

    food_info = [
        ("Good food (Eat)", FOOD_COLORS["good"]),
        ("Junk food (Pass)", FOOD_COLORS["bad"]),
        ("Raw food (Reject)", FOOD_COLORS["raw"])
    ]

    for i, (label, color) in enumerate(food_info):
        pygame.draw.rect(
            screen, color,
            (WIDTH // 2 - 80, food_legend_y + 30 + i * 22, 14, 14)
        )
        screen.blit(
            legend_font.render(label, True, (230, 230, 230)),
            (WIDTH // 2 - 60, food_legend_y + 28 + i * 22)
        )

    screen.blit(font.render(str(p1_size), True, (255, 255, 255)), (160, 520))
    screen.blit(font.render(str(p2_size), True, (255, 255, 255)), (510, 520))

    if not game_over:
        timer -= 1
        if timer <= 0:
            game_over = True

        if timer % (10 * FPS) == 0:
            food_speed += 0.5
            spawn_delay = max(25, spawn_delay - 5)

    timer_text = font.render(f"{timer // FPS}", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH // 2 - 20, 20))

    if game_over:
        if p1_size > p2_size:
            msg = "PLAYER 1 WINS"
        elif p2_size > p1_size:
            msg = "PLAYER 2 WINS"
        else:
            msg = "DRAW"

        text = font.render(msg, True, (255, 255, 255))
        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20)
        )

    pygame.display.flip()