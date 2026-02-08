import pygame
import random

class Player:
    def __init__(self, color, controls, dish_rect, image, reaction_images, start_size=300):
        self.color = color
        self.base_image = image       # Store the default image
        self.reaction_images = reaction_images # Store the dictionary of reactions
        self.controls = controls
        self.size = start_size
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.dish_rect = dish_rect
        self.current_dish = None
        
        # Animation variables
        self.offset_x = 0
        self.anim_state = None 
        self.target_dist = 0
        self.slide_speed = 25 

        self.stun_timer = 0 
        self.input_locked = False 

        # --- REACTION LOGIC ---
        self.reaction_timer = 0
        self.current_reaction_img = None

    def spawn_dish(self):
        self.current_dish = random.choice(["good", "bad", "spicy"])
        self.offset_x = 0
        self.anim_state = None

    def update(self):
        # Update Stun
        if self.stun_timer > 0:
            self.stun_timer -= 1
        
        # Update Reaction
        if self.reaction_timer > 0:
            self.reaction_timer -= 1
        else:
            self.current_reaction_img = None # Revert to normal face

    def handle_input(self, keys, table):
        # 1. EXIT EARLY: If stunned, animating, or no dish
        if not self.current_dish or self.anim_state or self.stun_timer > 0:
            return

        pressed_good = keys[self.controls["good"]]
        pressed_bad = keys[self.controls["bad"]]
        pressed_spicy = keys[self.controls["spicy"]]

        # If NO keys are currently pressed, unlock input
        if not (pressed_good or pressed_bad or pressed_spicy):
            self.input_locked = False
            return

        # If keys pressed but lock is on, return
        if self.input_locked:
            return

        self.input_locked = True
        dish = self.current_dish
        
        # --- 2. EATING LOGIC (Good/Up Key) ---
        if pressed_good:
            if dish == "good":
                self.size += 1
                self.current_dish = None 
                
                # REACTION: GOOD
                #self.current_reaction_img = self.reaction_images["good"]
                #self.reaction_timer = 30 # Show for 30 frames
                return 

            elif dish == "bad":
                self.size -= 1         
                self.current_dish = None 
                
                # REACTION: BAD
                self.current_reaction_img = self.reaction_images["bad"]
                self.reaction_timer = 30 # Show for 30 frames
                return

            elif dish == "spicy":
                self.stun_timer = 30    
                self.current_dish = None 
                
                # REACTION: SPICY (Lasts exactly as long as stun)
                self.current_reaction_img = self.reaction_images["spic"]
                self.reaction_timer = 30 
                return

        # --- 3. SORTING LOGIC ---
        if (pressed_bad and dish == "bad") or (pressed_spicy and dish == "spicy"):
            self.current_dish = None
            return

        # --- 4. ANIMATION LOGIC (Wrong sorting) ---
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

        # Phase 1: Slide OUT
        if self.anim_state == "out":
            if abs(self.offset_x) < abs(self.target_dist):
                direction = 1 if self.target_dist > 0 else -1
                self.offset_x += direction * self.slide_speed
            else:
                self.offset_x = self.target_dist 
                self.anim_state = "back"
        
        # Phase 2: Slide BACK
        elif self.anim_state == "back":
            if abs(self.offset_x) > 0:
                direction = -1 if self.offset_x > 0 else 1
                self.offset_x += direction * self.slide_speed
                if (direction == -1 and self.offset_x < 0) or (direction == 1 and self.offset_x > 0):
                    self.offset_x = 0
            else:
                self.offset_x = 0
                self.anim_state = None 

    def clamp(self):
        self.size = max(30, self.size)
        center = self.rect.center
        self.rect.size = (self.size, self.size)
        self.rect.center = center

    def draw(self, surface):
        # Decide which image to use: Reaction or Base
        img_source = self.base_image
        if self.reaction_timer > 0 and self.current_reaction_img:
            img_source = self.current_reaction_img

        # Scale it to current size
        img = pygame.transform.scale(
            img_source,
            self.rect.size
        )
        surface.blit(img, self.rect)

    def draw_dish(self, surface, food_images):
        if not self.current_dish:
            return

        img = food_images[self.current_dish]
        
        surface.blit(
            img,
            (
                (self.dish_rect.centerx + self.offset_x) - img.get_width() // 2,
                self.dish_rect.centery - img.get_height() // 2
            )
        )