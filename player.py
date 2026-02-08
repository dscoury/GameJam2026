import pygame
import random

class Player:
    def __init__(self, color, controls, dish_rect, start_size=50):
        self.color = color
        self.controls = controls
        self.size = start_size
        self.rect = pygame.Rect(0, 0, self.size, self.size)

        self.dish_rect = dish_rect
        self.current_dish = None

        # --- NEW ---
        self.dish_state = "idle"   # idle | out | back
        self.dish_pos = None
        self.dish_target = None
        self.dish_speed = 12
        self.input_locked = False
        self.failed_send = False

    def spawn_dish(self):
        self.current_dish = random.choice(["good", "bad", "spicy"])
        self.dish_state = "idle"
        self.dish_pos = pygame.Vector2(self.dish_rect.center)
        self.input_locked = False
        self.failed_send = False

    def handle_input(self, keys, targets):
        if not self.current_dish or self.input_locked:
            return

        dish = self.current_dish

        # ---------- WRONG EAT (instant, no sliding) ----------
        if dish != "good" and keys[self.controls["good"]]:
            self.size -= 4
            self.current_dish = None
            return

        # ---------- CORRECT EAT ----------
        if dish == "good" and keys[self.controls["good"]]:
            self.size += 5
            self.current_dish = None
            return

        # ---------- SENDING DISH ----------
        if keys[self.controls["bad"]]:
            self.start_send(
                target=targets["bad"],
                correct=(dish == "bad")
            )

        elif keys[self.controls["spicy"]]:
            self.start_send(
                target=targets["spicy"],
                correct=(dish == "spicy")
            )

    def start_send(self, target, correct):
        self.dish_target = pygame.Vector2(
            target[0],          # x from lady / trash
            self.dish_pos.y     # keep current y
        )

        self.dish_state = "out"
        self.input_locked = True
        self.failed_send = not correct

    def update_dish(self):
        if not self.current_dish or self.dish_state == "idle":
            return

        direction = self.dish_target - self.dish_pos
        distance = direction.length()

        if distance <= self.dish_speed:
            self.dish_pos = self.dish_target

            if self.dish_state == "out":
                if self.failed_send:
                    # Slide back
                    self.dish_target = pygame.Vector2(self.dish_rect.center)
                    self.dish_state = "back"
                else:
                    # Correct send → disappear
                    self.current_dish = None
                    self.input_locked = False

            elif self.dish_state == "back":
                self.dish_state = "idle"
                self.input_locked = False

        else:
            self.dish_pos += direction.normalize() * self.dish_speed

    def clamp(self):
        self.size = max(30, self.size)
        center = self.rect.center
        self.rect.size = (self.size, self.size)
        self.rect.center = center

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def draw_dish(self, surface, food_images):
        if not self.current_dish:
            return

        img = food_images[self.current_dish]
        surface.blit(
            img,
            (
                int(self.dish_pos.x - img.get_width() // 2),
                int(self.dish_pos.y - img.get_height() // 2)
            )
        )
