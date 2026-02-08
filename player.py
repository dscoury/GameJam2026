import random
import pygame


class Player:
    def __init__(self, color, controls, dish_rect, image, start_size = 300):
        self.color = color
        self.image = image
        self.controls = controls
        self.size = start_size
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.dish_rect = dish_rect
        self.current_dish = None
        
        # --- NEW ANIMATION VARIABLES ---
        self.offset_x = 0
        self.anim_state = None # None, "out", or "back"
        self.target_dist = 0
        self.slide_speed = 25 # Speed of the slide

        self.stun_timer = 0 
        self.input_locked = False # This flag prevents holding the button down

    def spawn_dish(self):
        self.current_dish = random.choice(["good", "bad", "spicy"])
        # Reset animation on spawn
        self.offset_x = 0
        self.anim_state = None

    # --- Call this every frame! ---
    def update(self):
        if self.stun_timer > 0:
            self.stun_timer -= 1

    def handle_input(self, keys, table):
        # 1. EXIT EARLY: If stunned, animating, or no dish, do nothing.
        if not self.current_dish or self.anim_state or self.stun_timer > 0:
            return

        pressed_good = keys[self.controls["good"]]
        pressed_bad = keys[self.controls["bad"]]
        pressed_spicy = keys[self.controls["spicy"]]

        # --- KEY RELEASE CHECK ---
        # If NO keys are currently pressed, we unlock the input
        if not (pressed_good or pressed_bad or pressed_spicy):
            self.input_locked = False
            return

        # If keys ARE pressed, but lock is still on (user hasn't let go yet), stop here.
        if self.input_locked:
            return

        # --- LOCK INPUT ---
        # We found a button press and we weren't locked. 
        # Lock it now so this action only happens once per press.
        self.input_locked = True

        dish = self.current_dish
        action_taken = False

        # --- 2. EATING LOGIC (The "W" or "UP" key) ---
        if pressed_good:
            action_taken = True
            if dish == "good":
                self.size += 1
                self.current_dish = None # Instant respawn
                return 
            elif dish == "bad":
                self.size -= 1          # Size penalty
                self.current_dish = None # Instant respawn (NO STUN)
                return
            elif dish == "spicy":
                self.stun_timer = 30    # STUN ONLY ON SPICY
                self.current_dish = None 
                return

        # --- 3. SORTING LOGIC (Correctly throwing away/giving away) ---
        if (pressed_bad and dish == "bad") or (pressed_spicy and dish == "spicy"):
            self.current_dish = None # Instant respawn
            return

        # --- 4. ANIMATION LOGIC (Pressing the wrong sorting key) ---
        target_x = None
        
        # Pressed Trash key for Good or Spicy food
        if pressed_bad and dish != "bad":
            if self.dish_rect.centerx < 400:
                target_x = table.trash_left.centerx
            else:
                target_x = table.trash_right.centerx

        # Pressed Lady key for Good or Bad food
        elif pressed_spicy and dish != "spicy":
            target_x = table.woman_rect.centerx

        if target_x is not None:
            self.anim_state = "out"
            self.target_dist = target_x - self.dish_rect.centerx

    def update_animation(self):
        if not self.anim_state:
            return

        # Phase 1: Slide OUT to target
        if self.anim_state == "out":
            # Move towards target
            if abs(self.offset_x) < abs(self.target_dist):
                direction = 1 if self.target_dist > 0 else -1
                self.offset_x += direction * self.slide_speed
            else:
                # Target reached, switch to sliding back
                self.offset_x = self.target_dist # Clamp
                self.anim_state = "back"
        
        # Phase 2: Slide BACK to plate
        elif self.anim_state == "back":
            if abs(self.offset_x) > 0:
                direction = -1 if self.offset_x > 0 else 1
                self.offset_x += direction * self.slide_speed
                # Snap to 0 if we overshot
                if (direction == -1 and self.offset_x < 0) or (direction == 1 and self.offset_x > 0):
                    self.offset_x = 0
            else:
                self.offset_x = 0
                self.anim_state = None # Animation finished

    def clamp(self):
        self.size = max(30, self.size)
        center = self.rect.center
        self.rect.size = (self.size, self.size)
        self.rect.center = center

    def draw(self, surface):
        img = pygame.transform.scale(
            self.image,
            self.rect.size
        )
        surface.blit(img, self.rect)

    def draw_dish(self, surface, food_images):
        if not self.current_dish:
            return

        img = food_images[self.current_dish]
        
        # ADD offset_x to the drawing position
        surface.blit(
            img,
            (
                (self.dish_rect.centerx + self.offset_x) - img.get_width() // 2,
                self.dish_rect.centery - img.get_height() // 2
            )
        )