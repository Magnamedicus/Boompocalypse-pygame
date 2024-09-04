import pygame
import random
class Player(pygame.sprite.Sprite):
    def __init__(self,game,player_pos):
        super().__init__()

        self.game = game
        self.player_pos = player_pos
        self.ground = game.ground
        self.player_health_max = 300
        self.player_health = 300000
        self.death_timer = 0
        self.shield = False
        self.shield_flipped = False
        self.player_shield_counter = 0
        self.shield_counter_counter = 0

        self.saw_blade = False
        self.saw_bleed_counter = 0



        self.player_move_v = [False, False]
        self.player_move_h = [False, False]

        self.player_velocity_y = 0
        self.player_velocity_h = 6.5
        self.player_velocity_p = 0
        self.knock_back_velocity_r = 0
        self.knock_back_velocity_l = 0
        self.upward_acceleration = False
        self.up_acceleration = 0.4
        self.knock_back_acceleration_r = 0.1
        self.knock_back_acceleration_l = 0.1
        self.jump_timer = 0


        self.player_run_counter = 0
        self.run_counter_counter = 0

        self.player_idle_counter = 0
        self.idle_counter_counter = 0

        self.player_jump_counter = 0

        self.player_death_counter = 0
        self.death_counter_counter = 0

        self.impact_alpha = 0
        self.laser_impact_counter = 0
        self.player_tint = False
        self.total_bombs_collected = 0




    def laser_hit_effect(self):
        self.laser_hit = True
        self.laser_hit_counter +=1
        if self.laser_hit_counter > 10:
            self.laser_hit = True

        return True













    def update(self):






        if self.shield == False and self.player_health > 0 and self.saw_blade == False:
            self.player_pos[0] += (self.player_move_h[1] - self.player_move_h[0]) * self.player_velocity_h
        else:

            self.player_pos[0] +=0

        self.player_pos[0] -= self.knock_back_velocity_r
        self.knock_back_velocity_r -= self.knock_back_acceleration_r
        if self.knock_back_velocity_r< 0:
            self.knock_back_velocity_r = 0

        self.player_pos[0] += self.knock_back_velocity_l
        self.knock_back_velocity_l -= self.knock_back_acceleration_l
        if self.knock_back_velocity_l < 0:
            self.knock_back_velocity_l = 0

        if self.player_pos[0] < 5:
            self.player_pos[0] = 5
        if self.player_pos[0] > self.game.info.current_w - 80:
            self.player_pos[0] = self.game.info.current_w - 80

        if self.player_health < 0:
            self.player_health = 0




        if self.player_move_h[1]:
            if self.shield == False:

                self.run_counter_counter += 1
                if self.run_counter_counter % 7 == 0:
                    self.player_run_counter += 1
                if self.player_run_counter > 5:
                    self.player_run_counter = 0

                if self.game.push:
                    self.image = self.game.hazmatt_push[self.player_run_counter]
                if not self.game.push and not self.game.laser_collide and self.player_health > 0 and not self.saw_blade:
                    self.image = self.game.player_ani_1[self.player_run_counter]
                if not self.game.push and not self.game.laser_collide and self.player_health > 0 and self.saw_blade:
                    self.saw_bleed_counter += 1
                    if self.saw_bleed_counter > 5:
                        self.saw_bleed_counter = 0
                    self.image = self.game.player_blood_saw[self.saw_bleed_counter]
                elif self.game.laser_collide:
                   self.image = self.game.player_ani_1_red[self.player_run_counter]
                   self.image.fill((0, 255, 255, 0), special_flags=pygame.BLEND_ADD)


            else:

                self.shield_counter_counter += 1
                if self.shield_counter_counter % 2 == 0:
                    self.player_shield_counter += 1

                    if self.player_shield_counter > 4:
                        self.player_shield_counter = 4

                self.image = self.game.hazmatt_shield[self.player_shield_counter]






        elif self.player_move_h[0]:


            self.run_counter_counter += 1
            if self.run_counter_counter % 7 == 0:
                self.player_run_counter +=1
            if self.player_run_counter > 5:
                self.player_run_counter = 0

            if self.game.push and not self.shield:
                self.image = self.game.hazmatt_push_flipped[self.player_run_counter]
            if not self.game.push and not self.shield and not self.game.laser_collide and self.player_health >0 and not self.saw_blade:
                self.image = self.game.player_ani_1_flipped[self.player_run_counter]
            if not self.game.push and not self.shield and not self.game.laser_collide and self.player_health >0 and self.saw_blade:
                self.saw_bleed_counter += 1
                if self.saw_bleed_counter > 5:
                    self.saw_bleed_counter = 0
                self.image = self.game.player_blood_saw_flipped[self.saw_bleed_counter]

            elif self.game.laser_collide and self.player_health > 0:
                self.image = self.game.player_ani_1_red_flipped[self.player_run_counter]
                self.image.fill((0, 255, 255, 0), special_flags=pygame.BLEND_ADD)

                #self.image.fill((self.impact_alpha, 0, 0, 190), special_flags=pygame.BLEND_ADD)
            if self.shield:
                self.shield_counter_counter += 1
                if self.shield_counter_counter % 2 == 0:
                    self.player_shield_counter += 1

                    if self.player_shield_counter > 4:
                        self.player_shield_counter = 4

                self.image = self.game.hazmatt_shield_flipped[self.player_shield_counter]

        elif self.shield:
            self.shield_counter_counter += 1
            if self.shield_counter_counter % 2 == 0:
                self.player_shield_counter += 1

                if self.player_shield_counter > 4:
                    self.player_shield_counter = 4

            self.image = self.game.hazmatt_shield[self.player_shield_counter]

        elif self.shield_flipped:
            self.shield_counter_counter += 1
            if self.shield_counter_counter % 2 == 0:
                self.player_shield_counter += 1

                if self.player_shield_counter > 4:
                    self.player_shield_counter = 4

            self.image = self.game.hazmatt_shield_flipped[self.player_shield_counter]

        elif self.saw_blade:
            self.player_health -= 5

            if self.rect.centerx < self.game.robot_mech.rect.centerx:
                self.saw_bleed_counter += 1
                if self.saw_bleed_counter > 5:
                    self.saw_bleed_counter = 0
                self.image = self.game.player_blood_saw[self.saw_bleed_counter]

            elif self.rect.centerx > self.game.robot_mech.rect.centerx:
                self.saw_bleed_counter += 1
                if self.saw_bleed_counter > 5:
                    self.saw_bleed_counter = 0
                self.image = self.game.player_blood_saw_flipped[self.saw_bleed_counter]






        else:

            self.idle_counter_counter += 1
            if self.idle_counter_counter % 8 == 0:
                self.player_idle_counter += 1
            if self.player_idle_counter > 57:
                self.player_idle_counter = 0
            if self.player_health >0 and not self.game.laser_collide:
                self.image = self.game.player_idle_load_1[self.player_idle_counter]
            elif self.game.laser_collide and self.player_health > 0:
                if self.player_idle_counter > 57:
                    self.player_idle_counter = 0
                self.image = self.game.player_idle_load_1_red[self.player_idle_counter]
                self.image.fill((0,255, 255, 0), special_flags=pygame.BLEND_ADD)
            if self.player_health > 0:
                self.rect = self.image.get_rect()


            #self.image.fill((190, 0, 0, 190), special_flags=pygame.BLEND_ADD)





        self.player_pos[1] -= self.player_velocity_y
        if self.upward_acceleration:
            self.player_velocity_y = 10
            self.player_velocity_y -= self.up_acceleration
            self.up_acceleration += 0.4
            self.jump_timer += 1
        if self.jump_timer > 50:
            self.jump_timer = 0
            self.upward_acceleration = False
            self.up_acceleration = 0
        if self.player_pos[1] > self.ground - 80:
            self.player_pos[1] = self.ground - 80

        if self.player_pos[1] < self.ground - 80:
            self.player_jump_counter +=1
        if self.player_pos[1] == self.ground - 80:
            self.player_jump_counter = 0

        if self.upward_acceleration:

            if self.player_jump_counter > 15:
                self.player_jump_counter = 15
            if not self.game.laser_collide:
                self.image = self.game.hazmatt_jump[self.player_jump_counter]
            elif self.game.laser_collide:
                self.image = self.game.hazmatt_jump_blue[self.player_jump_counter]
                self.image.fill((0, 255, 255, 0), special_flags=pygame.BLEND_ADD)

        if not self.upward_acceleration:
            self.jump_counter_counter = 0



        if self.upward_acceleration:
                if self.player_move_h[0] and self.shield_flipped == False:
                    if self.player_jump_counter > 15:
                        self.player_jump_counter = 15
                    if not self.game.laser_collide:
                        self.image = self.game.hazmatt_jump_left[self.player_jump_counter]
                    elif self.game.laser_collide:
                        self.image = self.game.hazmatt_jump_left_blue[self.player_jump_counter]
                        self.image.fill((0, 255, 255, 0), special_flags=pygame.BLEND_ADD)


        if not self.upward_acceleration:
            self.jump_counter_counter = 0

        #death animation
        if self.player_health == 0 and not self.upward_acceleration:
            self.rect.update(self.rect.centerx,self.rect.centery,0,0)
            self.player_pos[1] = self.ground - 60
            self.death_counter_counter+=1
            if self.death_counter_counter%3==0:
                self.player_death_counter +=1
                if self.player_death_counter > 62:
                    self.player_death_counter = 62
                self.image = self.game.hazmatt_death[self.player_death_counter]





        if self.player_health > 0:
            self.rect = self.image.get_rect()
        self.rect.x = self.player_pos[0]
        self.rect.y = self.player_pos[1]
        if not pygame.Rect.colliderect(self.game.player_1.rect, self.game.dumpster.rect):
            self.game.trash_truck.loading = False
        #self.image.fill((50,50,50))

        #dumpster stuff


        #if self.rect.right < self.game.dumpster.rect.left or self.rect.left > self.game.dumpster.rect.right:
            #if self.rect.right <= self.game.dumpster.rect.left and self.player_move_h[1]:

        if self.rect.colliderect(self.game.dumpster.rect) and self.game.push:
            if self.player_move_h[1]:
                if self.rect.right > self.game.dumpster.rect.left + 50:
                    self.rect.right = self.game.dumpster.rect.left + 50

                    self.player_velocity_p += 0.025
                    if self.player_velocity_p > 3.5:
                        self.player_velocity_p = 3.5
                    self.player_velocity_h = self.player_velocity_p
                    self.game.dumpster.dumpster_posx +=self.player_velocity_h
                    self.game.push_right = True
            elif self.player_move_h[0]:
                if self.rect.left < self.game.dumpster.rect.right - 32:
                    self.rect.left = self.game.dumpster.rect.right - 32
                    self.player_velocity_p += 0.025
                    if self.player_velocity_p > 3.5:
                        self.player_velocity_p = 3.5
                    self.player_velocity_h = self.player_velocity_p
                    self.game.dumpster.dumpster_posx -= self.player_velocity_h
                    self.game.push_left = True

        if not self.game.push:
            self.player_velocity_h = 6.5
            self.player_velocity_p = 0
            self.game.push_right = False
            self.game.push_left = False

            #self.image.fill((190, 0, 0, 190), special_flags=pygame.BLEND_ADD)






class Dumpster(pygame.sprite.Sprite):
    def __init__(self, game, dumpster_posx, dumpster_posy):
        super().__init__()
        self.game = game
        self.dumpster_posx = dumpster_posx
        self.dumpster_posy = dumpster_posy

        self.collected = 0
        self.emptied = 0

        self.image = pygame.image.load('images/Dumpster/empty_dumpster.png')

        self.image = pygame.transform.scale(self.image, (280, 170))
        self.rect = self.image.get_rect()

        self.rect.center = self.dumpster_posx,self.dumpster_posy




    def update(self):
        if self.dumpster_posx < (self.image.get_width()/2) * 1.4:
            self.dumpster_posx = (self.image.get_width()/2) * 1.4
        if self.dumpster_posx > self.game.info.current_w-(self.image.get_width()/2) * 1.4:
            self.dumpster_posx = self.game.info.current_w-(self.image.get_width()/2) * 1.4

        if self.collected >10 and self.collected <=20:
            self.image = pygame.image.load('images/Dumpster/dumpsterfill1.png')
        elif self.collected > 20 and self.collected <=30:
            self.image = pygame.image.load('images/Dumpster/dumpsterfill2.png')
        elif self.collected > 30:
            self.image = pygame.image.load('images/Dumpster/dumpsterfill3.png')
        else:
            self.image = pygame.image.load('images/Dumpster/empty_dumpster.png')

        if self.collected < 0:
            self.collected = 0



        self.image = pygame.transform.scale(self.image, (280, 170))
        self.rect = self.image.get_rect()
        self.rect.center = self.dumpster_posx, self.dumpster_posy

        if self.dumpster_posx > self.game.trash_truck_right.rect.left and self.game.trash_truck_right.velocity_right < 0:
            self.dumpster_posx = self.game.trash_truck_right.rect.left



class TrashTruck(pygame.sprite.Sprite):
    def __init__(self,game,pos_x,pos_y,side):
        super().__init__()
        self.game = game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_left = -4
        self.velocity_right = 4
        self.side = side
        self.truck_timer = 0
        self.truck_timer_right = 0
        self.ani_counter = 0
        self.ani_counter_counter = 0

        self.moving = False
        self.loading = False
        self.loading_time = 0

        self.right_rand_appear = 0
        self.left_rand_appear = 0




        self.image = pygame.image.load('images/trash_truck/trashtruck01.png')
        self.image = pygame.transform.scale(self.image, (880, 450))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos_x,self.pos_y




    def update(self):
        if self.side == 'Left':
            self.rect.centerx +=self.velocity_left
        if self.side == 'Right':
            self.rect.centerx +=self.velocity_right
        self.right_rand_appear = int(random.random()*2500)
        self.left_rand_appear = int(random.random()*2500)
        if self.side == "Left":
            if self.left_rand_appear == 200 and self.game.dumpster.collected > 20 and self.game.player_1.rect.centerx > self.game.screen_width/2 and self.game.trash_truck_right.rect.centerx > self.game.screen_width:
                self.velocity_left = 4
            #if self.game.dumpster.collected > 30 and not self.loading:
                #self.truck_timer += 1
            if self.rect.centerx > 300 and not self.loading:
                self.truck_timer +=1
            #if self.truck_timer > 300:
                #self.rect.centerx +=self.velocity
            if self.truck_timer == 700 or self.loading_time > 400:
                self.velocity_left = -self.velocity_left
                self.loading_time = 0
                self.truck_timer = 0

            if self.rect.centerx > 305:
                self.rect.centerx = 305

            if self.rect.centerx < -500:
                self.rect.centerx = -500


            if self.rect.centerx<305:

                self.ani_counter_counter +=1
                if self.ani_counter_counter%1==0:
                    if self.velocity_left > 0:
                        self.ani_counter +=1
                    elif self.velocity_left < 0:
                        self.ani_counter -=1
                if self.ani_counter > 14:
                    self.ani_counter = 0
                if self.ani_counter < 0:
                    self.ani_counter = 14
                self.image = self.game.trash_truck_move[self.ani_counter]


            if self.rect.centerx > 304:
                self.image = self.game.trash_truck_move[0]
                #self.image = pygame.image.load('images/trash_truck/trashtruck01.png')
                #self.image = pygame.transform.scale(self.image, (880, 450))




            if self.game.dumpster.dumpster_posx < self.rect.centerx + 375:
                self.game.dumpster.dumpster_posx = self.rect.centerx + 375

        #right side dumpster

        if self.side == 'Right':

            if self.right_rand_appear == 300 and self.game.dumpster.collected > 20 and self.truck_timer_right < 400 and self.game.player_1.rect.centerx < self.game.screen_width / 2 and self.game.trash_truck.rect.centerx < 0:
                self.velocity_right = -4

            if self.rect.centerx < self.game.screen_width - 305:
                self.rect.centerx = self.game.screen_width - 305
            if self.rect.centerx == self.game.screen_width - 305:
                self.truck_timer_right += 1
            if self.truck_timer_right > 700 or self.loading_time > 400:
                self.velocity_right = -self.velocity_right
                self.loading_time = 0
                self.truck_timer_right = 0



            if self.rect.centerx > self.game.screen_width + 450:
                self.rect.centerx = self.game.screen_width + 450
                self.truck_timer_right = 0

            if self.velocity_right < 0:
                self.ani_counter += 1
            elif self.velocity_right > 0:
                self.ani_counter -= 1
            if self.ani_counter > 14:
                self.ani_counter = 0
            if self.ani_counter < 0:
                self.ani_counter = 14
            if self.rect.centerx > self.game.screen_width - 305:
                self.image = self.game.trash_truck_move_flipped[self.ani_counter]
            else:
                self.image = self.game.trash_truck_move_flipped[0]







