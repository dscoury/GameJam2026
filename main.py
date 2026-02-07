import pygame
import random
import sys
import math

# SETUP

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
BASE_SURFACE = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sumo Growth DDR")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
legend_font = pygame.font.SysFont(None, 24)

# CONSTANTS

FPS = 60
GAME_LENGTH = 10 * FPS # 10 sekunder

TIMING_Y = 420
TIMING_HEIGHT = 24

LANES = {
    1: 200, # Player 1 lane (WASD)
    2: 550, # Player 2 lane (Piltaster)
}

FOOD_COLORS = {
    "good": (80, 220, 120),     # green
    "bad": (220, 80, 80),       # red
    "spicy": (200, 200, 200)      # gray
}

MISS_PENALTY = {
    "good": 4,
    "bad": 2,
    "spicy": 1
}

# PLAYER DATA

p1_size = 50
p2_size = 50

p1_rect = pygame.Rect(0, 0, 50, 50)
p2_rect = pygame.Rect(0, 0, 50, 50)

# FOOD

foods = []
spawn_timer = 0
spawn_delay = 60
food_speed = 4

def spawn_food():
    lane = random.choice([1, 2])
    food_type = random.choice(["good", "bad", "spicy"])
    rect = pygame.Rect(LANES[lane] - 15, -30, 30, 30)
    foods.append({
        "rect": rect,
        "type": food_type,
        "lane": lane
    })

# GAME STATE

timer = GAME_LENGTH
state = "PLAYING"

cutscene_timer = 0
push_phase = "warmup"

# SCREEN SHAKE
shake_intensity = 0
shake_timer = 0

# ZOOM
zoom = 1.0
TARGET_ZOOM = 1.15

# SOUND CHANT

"""def generate_chant():
    sound = pygame.sndarray.make_sound(
        (pygame.surfarray.array2d(
            pygame.Surface((200, 1))
        ) % 255).astype('int16')
    )
    return sound

try:
    chant_sound = generate_chant()

except:
    chant_sound = None"""

chant_sound = None 

# GAME LOOP

while True:
    clock.tick(FPS)
    BASE_SURFACE.fill((25, 25, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

    keys = pygame.key.get_pressed()

    # PLAYING STATE

    if state == "PLAYING":
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            spawn_food()
            spawn_timer = 0

        for food in foods[:]:
            food["rect"].y += food_speed
            in_zone = TIMING_Y <= food["rect"].y <= TIMING_Y + TIMING_HEIGHT

            # PLAYER 1

            if in_zone and food["lane"] == 1:
                if food["type"] == "good" and keys[pygame.K_w]:
                    p1_size += 5
                    foods.remove(food)

                elif food["type"] == "bad" and keys[pygame.K_a]:
                # Trash is to the LEFT
                    foods.remove(food)

                elif food["type"] == "spicy" and keys[pygame.K_d]:
                # Woman is towards the CENTER (right)
                    foods.remove(food)


            # PLAYER 2

            if in_zone and food["lane"] == 2:
                if food["type"] == "good" and keys[pygame.K_UP]:
                    p2_size += 5
                    foods.remove(food)

                elif food["type"] == "bad" and keys[pygame.K_RIGHT]:
                # Trash is to the RIGHT
                    foods.remove(food)

                elif food["type"] == "spicy" and keys[pygame.K_LEFT]:
                # Woman is towards the CENTER (left)
                    foods.remove(food)


            # MISS PENALTY

            if food in foods and food["rect"].y > TIMING_Y + TIMING_HEIGHT + 30:
                if food["lane"] == 1:
                    p1_size -= MISS_PENALTY[food["type"]]
                else:
                    p2_size -= MISS_PENALTY[food["type"]]
                foods.remove(food)

        timer -= 1
        if timer <= 0:
            state = "CUTSCENE"
            foods.clear()

            p1_rect.center = (WIDTH // 2 - 90, HEIGHT // 2)
            p2_rect.center = (WIDTH // 2 + 90, HEIGHT // 2)

            cutscene_timer = 0
            push_phase = "warmup"

            if chant_sound:
                chant_sound.play(-1)

        if timer % (10 * FPS) == 0:
            food_speed += 0.5
            spawn_delay = max(25, spawn_delay - 5)

    # CUTSCENE

    elif state == "CUTSCENE":
        cutscene_timer += 1
        zoom = min(TARGET_ZOOM, zoom + 0.002)

        if push_phase == "warmup":
            offset = 4 if (cutscene_timer // 15) % 2 == 0 else -4
            p1_rect.x += offset
            p2_rect.x -= offset

            if cutscene_timer > 120:
                push_phase = "final"
                shake_timer = 30
                shake_intensity = 10

        else:
            force = max(2, abs(p1_size - p2_size) // 10)
            if p1_size > p2_size:
                # PLAYER 1 pushes PLAYER 2 to the RIGHT
                p2_rect.x += force
            else:
                # PLAYER 2 pushes PLAYER 1 to the LEFT
                p1_rect.x -= force

        if p1_rect.right < 0 or p2_rect.left > WIDTH:
            state = "RESULT"
            if chant_sound:
                chant_sound.stop()
    
    # CLAMP SIZE

    p1_size = max(30, p1_size)
    p2_size = max(30, p2_size)

    p1_rect.size = (p1_size, p1_size)
    p2_rect.size = (p2_size, p2_size)

    # DRAW WORLD

    if state == "PLAYING":
        pygame.draw.rect(BASE_SURFACE, (200, 200, 0), (0, TIMING_Y, WIDTH, TIMING_HEIGHT))
        pygame.draw.line(BASE_SURFACE, (80, 80, 80), (400, 0), (400, HEIGHT), 2)

        for food in foods:
            pygame.draw.rect(BASE_SURFACE, FOOD_COLORS[food["type"]], food["rect"])
    
    pygame.draw.rect(BASE_SURFACE, (200, 80, 80), p1_rect)
    pygame.draw.rect(BASE_SURFACE, (80, 80, 220), p2_rect)

    # SHAKE AND ZOOM
    
    shake_x = shake_y = 0
    if shake_timer > 0:
        shake_timer -= 1
        shake_x = random.randint(-shake_intensity, shake_intensity)
        shake_y = random.randint(-shake_intensity, shake_intensity)

    scaled = pygame.transform.scale(
        BASE_SURFACE,
        (int(WIDTH * zoom), int(HEIGHT * zoom))
    )

    rect = scaled.get_rect(center=(WIDTH // 2 + shake_x, HEIGHT // 2 + shake_y))
    screen.fill((0, 0, 0))
    screen.blit(scaled, rect)

    # LEGEND AND INFO

    legend_p1 = [
        "PLAYER 1 (RED) - WASD",
        "W : Eat good food",
        "D : Pass junk food",
        "A : Reject spicy food"
    ]

    legend_p2 = [
        "PLAYER 2 (BLUE) - ARROWS",
        "UP    : Eat good food",
        "RIGHT : Pass junk food",
        "LEFT  : Reject spicy food"
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
        ("Spicy food (Reject)", FOOD_COLORS["spicy"])
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

    # SIZE TEXT

    screen.blit(font.render(str(p1_size), True, (255, 255, 255)), (160, 520))
    screen.blit(font.render(str(p2_size), True, (255, 255, 255)), (510, 520))

    # RESULT
    
    if state == "RESULT":
        winner = "DRAW"
        if p1_size > p2_size:
            winner = "PLAYER 1 WINS!"
        elif p2_size > p1_size:
            winner = "PLAYER 2 WINS!"

        text = font.render(winner, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))

    pygame.display.flip()