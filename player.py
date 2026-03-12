
# character reactions and size setup
# handles food input and following animations 

import pygame
import random


class Player:
    def __init__(self, color, controls, dish_rect, image, reaction_images, start_size=300):

        #player variables
        self.color = color
        self.base_image = image       # Store the default image 
        self.cached_image = None
        self.cached_size = None
        self.cached_source = None
        self.reaction_images = reaction_images # Store the dictionary of reactions
        self.reaction_timer = 0 
        self.current_reaction_img = None
        self.controls = controls   
        self.size = start_size
        self.rect = pygame.Rect(0, 0, self.size, self.size)

        # food variables
        self.dish_rect = dish_rect
        self.current_dish = None
        self.correct_delivery = False

        #food animation
        self.offset_x = 0
        self.anim_state = None 
        self.target_dist = 0
        self.slide_speed = 1200

        self.stun_timer = 0 
        self.input_locked = False 

        

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


    # INPUT LOGIC

    def handle_input(self, keys, table):
        # --- 1. EXIT EARLY: If stunned, animating, or no dish
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
        
        # --- 2. EATING LOGIC (Good/Up Key) 
        if pressed_good:
            if dish == "good":
                self.size += 1
                self.current_dish = None 
                
                # REACTION: GOOD
                self.current_reaction_img = self.reaction_images["good"]
                self.reaction_timer = 15 # Show for 30 frames
                return 

            elif dish == "bad":
                self.size -= 2     #minimizing size
                self.current_dish = None 
                
                # REACTION: BAD
                self.current_reaction_img = self.reaction_images["bad"]
                self.reaction_timer = 15 # Show for 30 frames
                return

            elif dish == "spicy":
                self.stun_timer = 45 # length of stun     
                self.current_dish = None 
                
                # REACTION: SPICY (Lasts exactly as long as stun)
                self.current_reaction_img = self.reaction_images["spicy"]
                self.reaction_timer = 45
                return


        # --- 3. SENDING FOOD LOGIC 

        target_x = None
        self.correct_delivery = False

        # Send to trash animation
        if pressed_bad:
            if self.dish_rect.centerx < 400:
                target_x = table.trash_left.centerx
            else:
                target_x = table.trash_right.centerx

            if dish == "bad":
                self.correct_delivery = True

        # send to lady animation
        elif pressed_spicy:
            target_x = table.woman_rect.centerx

            if dish == "spicy":
                self.correct_delivery = True

        # Start slide out animation
        if target_x is not None:
            self.anim_state = "out"
            self.target_dist = target_x - self.dish_rect.centerx


    def update_animation(self, dt):
        if not self.anim_state:
            return

        # Slide out food after input
        if self.anim_state == "out":
            if abs(self.offset_x) < abs(self.target_dist):
                direction = 1 if self.target_dist > 0 else -1
                self.offset_x += direction * self.slide_speed * dt
            else:
                self.offset_x = self.target_dist

                if self.correct_delivery:
                    # right placement == food disapears
                    self.current_dish = None
                    self.offset_x = 0
                    self.anim_state = None
                    self.correct_delivery = False
                else:
                    # wrong placement == food is sent back to players plate
                    self.anim_state = "back"

        # Slide back when food is sent wrong
        elif self.anim_state == "back":
            if abs(self.offset_x) > 0:
                direction = -1 if self.offset_x > 0 else 1
                self.offset_x += direction * self.slide_speed

                if (direction == -1 and self.offset_x < 0) or \
                (direction == 1 and self.offset_x > 0):
                    self.offset_x = 0
            else:
                self.offset_x = 0
                self.anim_state = None


    # shrinking and size change neutral
    def clamp(self):
        self.size = max(30, self.size)
        center = self.rect.center
        self.rect.size = (self.size, self.size)
        self.rect.center = center

    def draw(self, surface):

        img_source = self.base_image
        if self.reaction_timer > 0 and self.current_reaction_img:
            img_source = self.current_reaction_img

        # Only rescale if size OR image changed
        if (
            self.cached_size != self.rect.size
            or self.cached_source != img_source
            or self.cached_image is None
        ):
            self.cached_image = pygame.transform.scale(img_source, self.rect.size)
            self.cached_size = self.rect.size
            self.cached_source = img_source

        surface.blit(self.cached_image, self.rect)



    def draw_dish(self, surface, food_images):
        # Show dish
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

    #Reset for each round
    def reset(self, start_pos, start_size=300):

        self.size = start_size
        self.rect.size = (self.size, self.size)
        self.rect.center = start_pos

        self.current_dish = None

        self.offset_x = 0
        self.anim_state = None
        self.target_dist = 0

        self.stun_timer = 0
        self.input_locked = False

        self.reaction_timer = 0
        self.current_reaction_img = None
        self.cached_image = None

