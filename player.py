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

    def spawn_dish(self):
        self.current_dish = random.choice(["good", "bad", "spicy"])
        # Reset animation on spawn
        self.offset_x = 0
        self.anim_state = None

    # Update signature to accept 'table' so we know where to slide to
    def handle_input(self, keys, table):
        # Block input if no dish OR if currently animating
        if not self.current_dish or self.anim_state:
            return

        dish = self.current_dish

        # 1. HANDLE CORRECT MOVES (Existing Logic)
        if dish == "good" and keys[self.controls["good"]]:
            self.size += 1
            self.current_dish = None

        elif dish == "bad" and keys[self.controls["good"]]:
            self.size -= 1  # Decrease size
            self.current_dish = None  # Clear dish immediately (spawns new one next frame)



        elif dish == "bad" and keys[self.controls["bad"]]:
            self.current_dish = None
            #self.size -= 1
        elif dish == "spicy" and keys[self.controls["spicy"]]:
            self.current_dish = None
            
        # 2. HANDLE ANIMATION FOR WRONG MOVES (New Logic)
        else:
            target_x = None
            
            # Case: Player pressed TRASH key (Bad), but food is Good or Spicy
            if keys[self.controls["bad"]] and dish != "bad":
                # Find closest trash can (Left or Right)
                if self.dish_rect.centerx < 400: # Assuming center of screen is 400
                    target_x = table.trash_left.centerx
                else:
                    target_x = table.trash_right.centerx

            # Case: Player pressed LADY key (Spicy), but food is Good or Bad
            elif keys[self.controls["spicy"]] and dish != "spicy":
                target_x = table.woman_rect.centerx



            #Denne trenger vi ikke fordi jeg har lagt til en som gjør det samme over

            # Pressed GOOD key, but dish is Bad → penalize
            #elif keys[self.controls["good"]] and dish != "good":
            #    self.size -= 1



        # Could slide to some neutral spot or just keep original plate
                target_x = self.dish_rect.centerx + 50  # example

            # If a wrong move was detected, trigger animation
            if target_x is not None:
                self.anim_state = "out"
                # Calculate distance from dish to target
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
                self.anim_state = None # Animation finished, unlock input

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