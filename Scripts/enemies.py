import pygame
import random
import math

class Robot_Mech(pygame.sprite.Sprite):
    def __init__(self,game, pos_x, pos_y):
        super().__init__()
        self.game = game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.idle_counter = 0
        self.idle_counter_counter = 0
        self.missile_counter = 0

        self.combat_cycles = 0



        self.run_counter = 0
        self.run_counter_counter = 0

        self.image = self.game.robot_mech_idle[0]
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x,self.pos_y]

        self.velocity_h = 0
        self.velocity_v = 0
        self.idle = False
        self.combat_timer = 0
        self.saw_counter = 0
        self.idle_length = 0
        self.ticks = self.game.clock.tick(60)
        self.robot_acceleration = 0.25
        self.vertical_acceleration = 0.05
        self.v_accelerationChange = 0.001
        self.h_flight_acceleration = 0.05
        self.ground_behavior = True
        self.ground_vs_flight_rand = 0
        self.fly_cycles = 0

        self.number_of_flights = 0


        self.in_flight = False
        self.flight_trigger = 0

        self.fly_counter = 0
        self.flight_timer = 0
        self.landing_timer = 0



    def walk_around(self):
        robot_player_collide = self.rect.colliderect(self.game.player_1.rect)



        #basic walk mechanics
        #if 200 < self.rect.centerx < self.game.screen_width - 200:
            #self.rect.centerx += self.velocity_h
        #if self.rect.centerx < 250 or self.rect.centerx > self.game.screen_width-250:
            #self.velocity_h = -self.velocity_h
        if self.velocity_h < 0 and self.game.player_1.rect.centerx < self.rect.centerx and self.ground_behavior:
            self.run_counter_counter +=1
            if self.run_counter_counter%5 == 0:
                self.run_counter +=1
            if self.run_counter > 6:
                self.run_counter = 0
            self.image = self.game.robot_mech_walk[self.run_counter]
        elif self.velocity_h < 0 and self.game.player_1.rect.centerx > self.rect.centerx and self.ground_behavior:
            self.run_counter_counter += 1
            if self.run_counter_counter % 5 == 0:
                self.run_counter += 1
            if self.run_counter > 6:
                self.run_counter = 0
            self.image = self.game.robot_mech_reverse_flipped[self.run_counter]
        elif self.velocity_h > 0 and self.game.player_1.rect.centerx < self.rect.centerx and self.ground_behavior:
            self.run_counter_counter +=1
            if self.run_counter_counter%5 == 0:
                self.run_counter +=1
            if self.run_counter > 6:
                self.run_counter = 0
            self.image = self.game.robot_mech_reverse[self.run_counter]
        elif self.velocity_h > 0 and self.game.player_1.rect.centerx > self.rect.centerx and self.ground_behavior:
            self.run_counter_counter += 1
            if self.run_counter_counter % 5 == 0:
                self.run_counter += 1
            if self.run_counter > 6:
                self.run_counter = 0
            self.image = self.game.robot_mech_walk_flipped[self.run_counter]

        elif self.velocity_h == 0 and not robot_player_collide and self.ground_behavior:
            self.idle_counter_counter += 1
            if self.idle_counter_counter % 20 == 0:
                self.idle_counter += 1
            if self.idle_counter > 5:
                self.idle_counter = 5
            if self.rect.centerx > self.game.player_1.rect.centerx:
                #self.image = self.game.robot_mech_idle[self.idle_counter]
                self.image = self.game.robot_mech_shoot[self.idle_counter]
            elif self.rect.centerx < self.game.player_1.rect.centerx and self.in_flight == False:
                #self.image = self.game.robot_mech_idle_flipped[self.idle_counter]
                self.image = self.game.robot_mech_shoot_flipped[self.idle_counter]


        if robot_player_collide and self.velocity_h == 0 and self.ground_behavior:
            self.game.player_1.saw_blade = True
            self.saw_counter +=1
            if self.saw_counter > 29:
                self.saw_counter = 17
            if self.game.player_1.rect.centerx < self.rect.centerx:
                self.image = self.game.robot_saw[self.saw_counter]
            elif self.game.player_1.rect.centerx > self.rect.centerx and self.ground_behavior:
                self.image = self.game.robot_saw_flipped[self.saw_counter]
        else:
            self.game.player_1.saw_blade = False
        if self.velocity_h !=0:
            self.idle_counter = 0
        if not robot_player_collide:
            self.saw_counter = 0

        if self.in_flight:
            self.fly_counter += 1
            if self.fly_counter > 11:
                self.fly_counter = 4
            if self.game.player_1.rect.centerx < self.rect.centerx:
                self.image = self.game.robot_fly[self.fly_counter]
            elif self.game.player_1.rect.centerx > self.rect.centerx:
                self.image = self.game.robot_fly_flipped[self.fly_counter]



    def landing_sequence(self):
        if self.in_flight:
            if self.fly_cycles >= 200:
                self.ground_behavior = False
                self.rect.centerx += self.velocity_h



                if self.rect.y < 100:
                    self.rect.y = 100
                    self.vertical_acceleration = -0.05

                if self.vertical_acceleration < - 0.1:
                    self.v_accelerationChange = -self.v_accelerationChange
                if self.in_flight:
                    self.landing_timer += 1 / (self.ticks +4)


                if 0 < self.landing_timer < 5:
                    if self.rect.centerx > 200 and self.rect.centerx < self.game.screen_width - 200:
                        if self.velocity_h > 0:
                            self.velocity_h -= 0.05
                        elif self.velocity_h < 0:
                            self.velocity_h += 0.05

                        if -0.5 < self.velocity_h < 0.5:
                            self.velocity_h = 0


                if self.landing_timer > 5:
                    if self.rect.centery < 728:
                        self.rect.centery += 1.5
                if self.rect.centery == 728:

                    self.in_flight = False
                    self.ground_behavior = True







    def fly_around(self):

        if self.fly_cycles < 200:
            if self.flight_timer > 5:
                self.ground_vs_flight_rand = random.randint(1,10000)
                if self.ground_vs_flight_rand in [5000,6000,7000]:

                    self.ground_behavior = True
                elif 1 < self.ground_vs_flight_rand < 500:
                    self.ground_behavior = False

            #vertical hovering behavior
            if self.rect.y < 100:
                self.rect.y = 100
                self.vertical_acceleration = -0.05

            if self.vertical_acceleration < - 0.1:
                self.v_accelerationChange = -self.v_accelerationChange
            if self.in_flight:
                self.flight_timer += 1 / (self.ticks +4)
                if self.flight_timer > 45:
                    self.flight_timer = 5




            if self.in_flight:
                self.rect.centery -= self.velocity_v
                self.velocity_v += self.vertical_acceleration

                if self.rect.centery < 250:
                    self.vertical_acceleration -= self.v_accelerationChange

                if self.flight_timer > 5:
                    if self.rect.centery > self.game.screen_height - 550:
                        self.vertical_acceleration = 0.05

                #In flight, horizontal movement behavior
                if 5 < self.flight_timer < 10 and self.ground_behavior == False:

                    self.velocity_h += self.h_flight_acceleration
                    self.rect.centerx += self.velocity_h
                    if self.velocity_h > 6:
                        self.velocity_h = self.velocity_h/2


                if 10 < self.flight_timer < 35 and self.ground_behavior == False:
                    if not self.rect.centerx < 100:
                        self.h_flight_acceleration = 0.08
                        self.velocity_h -= self.h_flight_acceleration
                        self.rect.centerx += self.velocity_h
                        if self.velocity_h < -9:
                            self.velocity_h = -9
                    if self.rect.centerx < self.game.screen_width/2:
                        self.h_flight_acceleration = 0.14
                        self.velocity_h += self.h_flight_acceleration
                    if self.rect.centerx <= 100:
                        self.velocity_h = 0

                if 35 < self.flight_timer < 37 and self.ground_behavior == False:
                        self.h_flight_acceleration = 0.05
                        self.velocity_h += self.h_flight_acceleration
                        self.rect.centerx += self.velocity_h
                if self.flight_timer == 38:
                    self.velocity_h = 0


                if self.flight_timer > 40 and self.ground_behavior == False:
                    self.fly_cycles += 1


                    self.h_flight_acceleration = 0.06
                    self.velocity_h -= self.h_flight_acceleration

                    self.rect.centerx -= self.velocity_h








                #if self.rect.centerx < 250 or self.rect.centerx > self.game.screen_width - 250:
                    #self.velocity_h = 0












    def shoot_laser(self,game,x,y,from_spaceship):
        return SpaceshipLaser(game,x,y, from_spaceship)


    def shoot_missile(self):
        return Missile(self.game,self.rect.centerx,self.rect.centery)







    def update(self):

        if self.in_flight == False and self.number_of_flights == 0 and self.combat_cycles == 3:


            self.fly_cycles = 0
            self.in_flight = True
            self.number_of_flights +=1

        if self.in_flight:
            self.missile_counter = random.randint(1,2000)



        self.combat_timer += 1 / (self.ticks * 4)
        if self.combat_timer > 15:
            self.combat_timer = 0
            self.combat_cycles +=1









        if self.velocity_h == 0:
            self.idle = True
        else:
            self.idle = False

        if self.idle:

            self.idle_counter_counter +=1
            if self.idle_counter_counter%3 == 0:
                self.idle_counter +=1
            if self.idle_counter > 44:
                self.idle_counter = 0
            #if self.rect.centerx > self.game.player_1.rect.centerx:
                #self.image = self.game.robot_mech_idle[self.idle_counter]
                #self.image = self.game.robot_mech_shoot[0]
            #elif self.rect.centerx < self.game.player_1.rect.centerx:
                #self.image = self.game.robot_mech_idle_flipped[self.idle_counter]
                #self.image = self.game.robot_mech_shoot_flipped[0]

        if self.game.mech_active:
            self.walk_around()

        if self.in_flight and self.game.mech_active:
            self.fly_around()
            self.landing_sequence()

        if self.ground_behavior and self.game.mech_active:

            if 0 < self.combat_timer < 3:
                if not self.rect.centerx < 250 and not self.rect.centerx > self.game.screen_width - 250:
                    self.velocity_h = 5
                self.rect.centerx += self.velocity_h
                if self.rect.centerx < 250 or self.rect.centerx > self.game.screen_width - 250:
                    self.velocity_h = 0

            if 3 <= self.combat_timer < 7:
                if not self.rect.centerx < 250:
                    self.velocity_h = -8
                self.rect.centerx += self.velocity_h
                self.rect.centerx += self.velocity_h
                if self.rect.centerx < 250 or self.rect.centerx > self.game.screen_width - 250:
                    self.velocity_h = 0

            if 7 <= self.combat_timer < 11:
                if abs(self.rect.centerx - self.game.player_1.rect.centerx) > 200:
                    if self.rect.centerx < self.game.player_1.rect.centerx:
                        self.velocity_h += 0.08
                        self.rect.centerx += self.velocity_h
                    elif self.rect.centerx > self.game.player_1.rect.centerx:
                        self.velocity_h -= 0.08
                        self.rect.centerx += self.velocity_h

                elif abs(self.rect.centerx - self.game.player_1.rect.centerx) <= 200:
                    self.velocity_h = 0

            if 11 <= self.combat_timer < 15:


                if self.rect.centerx < self.game.player_1.rect.centerx:
                    self.rect.centerx += self.velocity_h
                    self.velocity_h -= self.robot_acceleration
                elif self.rect.centerx > self.game.player_1.rect.centerx:
                    self.rect.centerx += self.velocity_h
                    self.velocity_h += self.robot_acceleration
                if self.rect.centerx < 250 and self.game.player_1.rect.centerx > self.rect.centerx:
                    self.velocity_h = 0
                if self.rect.centerx > self.game.screen_width - 230 and self.game.player_1.rect.centerx < self.rect.centerx:
                    self.velocity_h = 0











class AlienFighter(pygame.sprite.Sprite):
    def __init__(self,game, pos_x, pos_y):
        super().__init__()
        self.game = game
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.ani_counter = 0
        self.ani_counter_counter = 0

        self.engage_timer = 0
        self.image = self.game.alien_fighter_left[0]
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x,self.pos_y]

        self.velocity_h = 0
        self.velocity_v = 0

        self.left_face = False
        self.right_face = False

        self.nuke_rand = 0
        self.shoot_rand = 0
        self.rand_appear = 0

        self.acceleration_h = 0.1

        self.engage = False
        self.appear = False
        self.leave = False
        self.stay_length = 1500

    def entrance(self):
        if not self.engage:
            self.rect.centerx += self.velocity_h

            if self.rect.centerx > self.game.player_1.rect.centerx + 100:
                self.velocity_h -= 0.05
                if self.velocity_h < -3:
                    self.velocity_h = -3
                self.ani_counter_counter += 1
                if self.ani_counter_counter % 4 == 0:
                    self.ani_counter += 1
                    self.image = self.game.alien_fighter_left[self.ani_counter]
                    if self.ani_counter > 32:
                        self.ani_counter = 0
            if self.rect.centerx < self.game.screen_width - 50:
                self.rect.centerx = self.game.screen_width - 50
                self.engage = True



    def fly_around(self):
        self.rect.centerx += self.velocity_h

        if self.rect.centerx > self.game.player_1.rect.centerx +100:
            if self.engage_timer<self.stay_length:
                self.velocity_h -= 0.05
                if self.velocity_h < -5:
                    self.velocity_h = -5
            if self.engage_timer >=self.stay_length:
                self.velocity_h = 5
                if self.rect.centerx > self.game.screen_width + 250:
                    self.rect.centerx = self.game.screen_width + 250
                    self.engage = False
                    self.engage_timer = 0
            if self.engage_timer < self.stay_length:
                self.ani_counter_counter += 1
                if self.ani_counter_counter % 4 == 0:
                    self.ani_counter += 1
                    self.image = self.game.alien_fighter_left[self.ani_counter]
                    if self.ani_counter > 32:
                        self.ani_counter = 0
        elif self.rect.centerx < self.game.player_1.rect.centerx -100:
            self.velocity_h += 0.05
            if self.velocity_h > 5:
                self.velocity_h = 5
            self.ani_counter_counter += 1
            if self.ani_counter_counter % 4 == 0:
                self.ani_counter += 1
                self.image = self.game.alien_fighter_right[self.ani_counter]
                if self.ani_counter > 32:
                    self.ani_counter = 0

        elif self.game.player_1.rect.centerx -10 < self.rect.centerx < self.game.player_1.rect.centerx + 10:
            self.velocity_h = 0


        if self.rect.centerx < 0 or self.rect.centerx > self.game.screen_width and self.engage_timer<self.stay_length:
            self.velocity_h = -self.velocity_h


        if abs(self.rect.centerx - self.game.player_1.rect.centerx) > 300:
            self.rect.centery += 4
        else:
            self.rect.centery -=4

        if self.rect.centery > 550:
            self.rect.centery = 550
        if self.rect.centery < 200:
            self.rect.centery = 200

    def shoot_laser(self):
        return SpaceshipLaser(self.game,self.rect.centerx,self.rect.centery-50,True)

    def create_nuke(self):


        return NuclearBomb(self.game,self.game.alien_fighter.rect.centerx,self.game.alien_fighter.rect.centery)





    def update(self):
        if self.appear == False:
            self.rand_appear = random.randint(0,1000)
        if self.game.dumpster.collected > 25 and self.rand_appear == 500 and self.appear == False:
            self.appear = True
        if self.appear:
            self.entrance()

        if self.engage:
            self.engage_timer +=1
            self.appear = False
            self.fly_around()
            if self.engage_timer < self.stay_length:
                self.nuke_rand = int(random.randint(1, 500))
                self.shoot_rand_rand = int(random.randint(1, 500))

            if self.velocity_h < 0:
                self.left_face = True
                self.right_face = False
            if self.velocity_h > 0:
                self.left_face = False
                self.right_face = True
            if self.left_face:
                self.ani_counter_counter += 1
                if self.ani_counter_counter % 4 == 0:
                    self.ani_counter += 1
                    self.image = self.game.alien_fighter_left[self.ani_counter]
                    if self.ani_counter > 32:
                        self.ani_counter = 0
            if self.right_face:
                self.ani_counter_counter += 1
                if self.ani_counter_counter % 4 == 0:
                    self.ani_counter += 1
                    self.image = self.game.alien_fighter_right[self.ani_counter]
                    if self.ani_counter > 32:
                        self.ani_counter = 0

class Missile(pygame.sprite.Sprite):
    def __init__(self,game,pos_x,pos_y):
        super().__init__()
        self.game = game
        self.startx = pos_x
        self.starty = pos_y
        self.missile_left = False
        self.missile_right = False
        self.projectile_speed = 30
        self.unexploded = True

        self.ani_counter = 0
        self.explosion_counter = 0
        self.explosion_counter_counter = 0



        self.image = pygame.image.load('images/missile_ani/missile02.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (160, 45))

        self.angle = self.angle_to_target(self.game.robot_mech, self.game.player_1)
        self.image = pygame.transform.rotate(self.image, self.angle)

        self.projectile_dx = self.projectile_speed * math.cos(math.radians(self.angle))
        self.projectile_dy = -self.projectile_speed * math.sin(math.radians(self.angle))

        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x + 10
        self.rect.centery = pos_y -40

    def angle_to_target(self, origin, target):
        dx = (target.rect.centerx) - origin.rect.centerx
        dy = (target.rect.centery) - origin.rect.centery
        radians = math.atan2(-dy, dx)
        angle = math.degrees(radians)
        return angle

    def update(self):


        if self.unexploded:
            self.rect.centerx += self.projectile_dx
            self.rect.centery += self.projectile_dy


        if self.rect.centery > self.game.ground-10:
            self.unexploded = False

            self.explosion_counter_counter +=1
            if self.explosion_counter_counter%2 ==0:

                self.explosion_counter +=1
                if self.explosion_counter > 14:
                    self.explosion_counter = 14
                    self.kill()
            self.image = self.game.nuke_explode[self.explosion_counter]


        if self.game.player_1.player_health > 0:
            if  self.rect.centery > (self.game.ground-10) and (self.rect.centerx - self.game.player_1.player_pos[0])>0:
                is_hit_right = pygame.Rect.colliderect(self.rect,self.game.player_1.rect)
                if is_hit_right or (self.rect.x - self.game.player_1.player_pos[0])<50 and not self.game.player_1.shield:
                    self.game.player_1.knock_back_velocity_r = 10
                    if self.game.player_1.image != self.game.hazmatt_shield[4]:
                        self.game.player_1.upward_acceleration = True
                    if self.game.player_1.shield and self.game.player_1.image == self.game.hazmatt_shield[4]:
                        self.game.player_1.player_health -=5
                        self.game.player_1.knock_back_velocity_r = 5
                    else:
                        self.game.player_1.player_health -=10

            if self.rect.centery > (self.game.ground -10) and (self.rect.centerx - self.game.player_1.player_pos[0])<0:
                is_hit_left = pygame.Rect.colliderect(self.rect,self.game.player_1.rect)
                if is_hit_left or abs((self.rect.x - self.game.player_1.player_pos[0]))<50 and not self.game.player_1.shield:
                    self.game.player_1.knock_back_velocity_l = 10
                    if self.game.player_1.image != self.game.hazmatt_shield_flipped[4]:
                        self.game.player_1.upward_acceleration = True
                    if self.game.player_1.shield and self.game.player_1.player_move_h[0] and self.game.player_1.image == self.game.hazmatt_shield_flipped[4]:
                        self.game.player_1.player_health -=5
                        self.game.player_1.knock_back_velocity_l = 5

                    else:
                        self.game.player_1.player_health -=10



        #if self.rect.centery > self.game.ground:
            #self.rect.centery = self.game.ground

            #self.kill()





class SpaceshipLaser(pygame.sprite.Sprite):
    def __init__(self,game, pos_x, pos_y,from_spaceship):
        super().__init__()
        self.game = game
        self.startx = pos_x
        self.starty = pos_y
        self.from_spaceship = from_spaceship
        if self.from_spaceship:
            self.image = pygame.image.load('images/blue_laser_template.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,(self.game.screen_width * 0.03835, self.game.screen_height * 0.01097))
            self.angle = self.angle_to_target(self.game.alien_fighter, self.game.player_1)
            self.image = pygame.transform.rotate(self.image, self.angle)
        elif not self.from_spaceship:

            if self.startx < self.game.player_1.rect.centerx:
                self.image = pygame.image.load('images/robot_laser.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (
                self.game.screen_width * 0.05835, self.game.screen_height * 0.03097))
            if self.startx > self.game.player_1.rect.centerx:
                self.image = pygame.image.load('images/robot_laser.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (
                self.game.screen_width * 0.05835, self.game.screen_height * 0.03097))
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.image.load('images/blank.png')



        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
        self.blue_laser_impact_counter = 0
        self.blue_laser_impact_counter_counter = 0
        self.projectile_speed = 40
        self.player_hit = False
        self.hit_timer = 0

        self.left = False
        self.right = False

        self.invisible = False
        self.rotate_counter = 0




    def angle_to_target(self,origin, target):
        dx = (target.rect.centerx + random.random()*100) - origin.rect.centerx
        dy = (target.rect.centery + random.random()*100) - (origin.rect.centery)
        radians = math.atan2(-dy, dx)
        angle = math.degrees(radians)
        return angle



    def update(self):


        if self.from_spaceship:

            self.rotate_counter +=1






            angle = self.angle_to_target(self.game.alien_fighter, self.game.player_1)



            projectile_dx = self.projectile_speed/2 * math.cos(math.radians(angle))
            projectile_dy = -self.projectile_speed/2 * math.sin(math.radians(angle))



            self.rect.centerx += projectile_dx
            self.rect.centery += projectile_dy

        if not self.from_spaceship:
            if self.startx < self.game.player_1.rect.centerx and not self.right:
                self.left = True
            if self.left:
                self.rect.centerx += self.projectile_speed
                self.image = pygame.image.load('images/robot_laser.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.game.screen_width * 0.05835, self.game.screen_height * 0.03097))

            if self.startx > self.game.player_1.rect.centerx and not self.left:
                self.right = True
            if self.right:
                self.rect.centerx -= self.projectile_speed
                self.image = pygame.image.load('images/robot_laser.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.game.screen_width * 0.05835, self.game.screen_height * 0.03097))
                self.image = pygame.transform.flip(self.image, True, False)

            if self.rect.colliderect(self.game.player_1.rect) and not self.game.player_1.shield:
                self.game.player_1.player_health -= 5
                self.invisible = True
            if self.invisible:
                self.image.set_alpha(0)







        laser_player_collide = self.rect.colliderect(self.game.player_1.rect)
        if laser_player_collide and self.game.player_1.shield:
            self.projectile_speed = 0


            self.blue_laser_impact_counter_counter +=1

            self.player_hit = True
            if self.blue_laser_impact_counter_counter %2 == 0:
                self.blue_laser_impact_counter += 1
            if self.blue_laser_impact_counter > 5:
                self.blue_laser_impact_counter = 5

                self.kill()
            self.image = self.game.blue_laser_impact[self.blue_laser_impact_counter]
        if not self.rect.colliderect(self.game.player_1.rect) and self.player_hit == True:
            self.kill()

        if self.rect.colliderect(self.game.player_1.rect) and not self.game.player_1.shield:
            self.image.set_alpha(0)



















        if self.rect.centery > self.game.screen_height or self.rect.centerx < 0 or self.rect.centerx > self.game.screen_width:

            self.kill()




class NuclearBomb(pygame.sprite.Sprite):
    def __init__(self,game, pos_x, pos_y):
        super().__init__()
        self.game = game
        self.image = self.game.nuclear_bomb[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = pos_y

        self.velocity = 13

        self.ani_counter = 0
        self.ani_counter_counter = 0

        self.explosion_counter = 0
        self.explosion_counter_counter = 0

        self.player_distance_real = self.rect.centerx - self.game.player_1.rect.centerx




    def update(self):

        self.rect.centery +=self.velocity
        self.velocity += 1
        if self.rect.y > (self.game.screen_height - 180):
            self.rect.y = (self.game.screen_height - 180)
        if self.velocity >13:
            self.velocity = 13
        if self.game.alien_fighter.right_face:
            self.ani_counter_counter+=1
            if self.ani_counter_counter %2==0:
                self.ani_counter +=1
            if self.ani_counter > 15:
                self.ani_counter = 15
            self.image = self.game.nuclear_bomb[self.ani_counter]
        elif self.game.alien_fighter.left_face:
            self.ani_counter_counter += 1
            if self.ani_counter_counter % 2 == 0:
                self.ani_counter += 1
            if self.ani_counter > 15:
                self.ani_counter = 15
            self.image = self.game.nuclear_bomb_flipped[self.ani_counter]


        if self.rect.y == (self.game.screen_height - 180):
            self.explosion_counter_counter +=1
            if self.explosion_counter_counter%2 ==0:

                self.explosion_counter +=1
                if self.explosion_counter > 14:
                    self.explosion_counter = 14
                    self.kill()
            self.image = self.game.nuke_explode[self.explosion_counter]

        if self.game.player_1.player_health > 0:
            if  self.rect.y == (self.game.screen_height - 180) and (self.rect.x - self.game.player_1.player_pos[0])>0:
                is_hit_right = pygame.Rect.colliderect(self.rect,self.game.player_1.rect)
                if is_hit_right or (self.rect.x - self.game.player_1.player_pos[0])<200 and not self.game.player_1.shield:
                    self.game.player_1.knock_back_velocity_r = 10
                    if self.game.player_1.image != self.game.hazmatt_shield[4]:
                        self.game.player_1.upward_acceleration = True
                    if self.game.player_1.shield and self.game.player_1.image == self.game.hazmatt_shield[4]:
                        self.game.player_1.player_health -=5
                        self.game.player_1.knock_back_velocity_r = 5
                    else:
                        self.game.player_1.player_health -=10

            if self.rect.y == (self.game.screen_height - 180) and (self.rect.x - self.game.player_1.player_pos[0])<0:
                is_hit_left = pygame.Rect.colliderect(self.rect,self.game.player_1.rect)
                if is_hit_left or abs((self.rect.x - self.game.player_1.player_pos[0]))<200 and not self.game.player_1.shield:
                    self.game.player_1.knock_back_velocity_l = 10
                    if self.game.player_1.image != self.game.hazmatt_shield_flipped[4]:
                        self.game.player_1.upward_acceleration = True
                    if self.game.player_1.shield and self.game.player_1.player_move_h[0] and self.game.player_1.image == self.game.hazmatt_shield_flipped[4]:
                        self.game.player_1.player_health -=5
                        self.game.player_1.knock_back_velocity_l = 5

                    else:
                        self.game.player_1.player_health -=10








class Spaceship(pygame.sprite.Sprite):
    def __init__(self,game, width, height, pos_x, pos_y):
        super().__init__()
        self.game = game
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.ani_counter = 0
        self.ani_counter_counter = 0


        self.image = self.game.spaceship_ani[0]
        #self.image = pygame.image.load('images/enemy1.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))



        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x,self.pos_y]

        self.velocity_h = 2
        self.velocity_v = 1
        self.space_ship_behave = 0


    def update(self):
        self.ani_counter_counter +=1
        if self.ani_counter_counter > 1000:
            self.ani_counter_counter = 0
        if self.ani_counter_counter%8==0:
            self.ani_counter+=1
            if self.ani_counter > 2:
                self.ani_counter = 0
        self.image = self.game.spaceship_ani[self.ani_counter]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))



        if self.game.game_timer > 12.0:
            self.space_ship_behave = random.randint(1, 10000)
            self.rect.x += self.velocity_h
            self.rect.y += self.velocity_v

            if self.rect.x > self.game.info.current_w - (self.game.info.current_w * 0.2) or self.rect.x < 50:
                self.velocity_h = -self.velocity_h
            if self.space_ship_behave % 500 == 0:
                self.velocity_h = -self.velocity_h

            if self.rect.y > (self.game.info.current_h - (self.game.info.current_h * 0.60)) or self.rect.y < -5:
                self.velocity_v = -self.velocity_v
            if self.space_ship_behave % 75 == 0:
                self.velocity_v = -self.velocity_v
        if self.game.game_timer > 8 and self.game.game_timer < 12.0:
            self.rect.y +=1

    def create_bomb(self):

        return Bomb(self.game,self,self.game.spaceship.rect.centerx-10,self.game.spaceship.rect.centery)

class Bomb(pygame.sprite.Sprite):
    def __init__(self,game,ship, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('images/bomb.png')
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.image_red = pygame.image.load('images/bomb_red.png')
        self.image_red = pygame.transform.scale(self.image_red, (50, 50))

        #self.image.fill((0,0,0))
        self.game = game
        self.ship = ship
        self.rect = self.image.get_rect()


        self.rect.x = pos_x
        self.rect.y = pos_y

        self.bounce_counter = 0
        self.bomb_acceleration = 0.25

        self.velocity_max = 10
        self.velocity_min = 0

        self.velocity = random.randint(self.velocity_min,self.velocity_max)
        self.velocity_h = random.randint(self.velocity_min,self.velocity_max)
        self.bomb_right = False
        self.bomb_left = False

        if self.ship.rect.x > 500:
            self.bomb_left = True
        else:
            self.bomb_left = False
            self.bomb_right = True

        self.explosion_counter = 0
        self.explosion_counter_counter = 0

        self.player_distance_real = self.rect.centerx - self.game.player_1.rect.centerx
        self.player_distance_abs = abs(self.player_distance_real)







    def update(self):
        self.rect.y += self.velocity




        if self.rect.y > self.game.info.current_h - (self.game.info.current_h * 0.08):
            self.velocity = self.velocity* -1



        if self.velocity <=0:
            self.velocity += self.bomb_acceleration


        if self.rect.y < self.game.info.current_h - (self.game.info.current_h * 0.065) and self.bomb_right == True:
            self.rect.x += self.velocity_h
        if self.rect.y < self.game.info.current_h - (self.game.info.current_h * 0.065) and self.bomb_left == True:
            self.rect.x -= self.velocity_h



        if self.rect.y > self.game.info.current_h - (self.game.info.current_h * 0.25):
            self.bounce_counter +=1


        self.velocity += self.bomb_acceleration

        #Player effect when bombs explode
        if self.game.player_1.player_health > 0:
            if self.bounce_counter > 400 and (self.rect.x - self.game.player_1.player_pos[0])>0:
                is_hit_right = pygame.Rect.colliderect(self.rect,self.game.player_1.rect)
                if is_hit_right or (self.rect.x - self.game.player_1.player_pos[0])<200:
                    self.game.player_1.knock_back_velocity_r = 10
                    self.game.player_1.upward_acceleration = True
                    self.game.player_1.player_health -=10

            if self.bounce_counter > 400 and (self.rect.x - self.game.player_1.player_pos[0])<0:
                is_hit_left = pygame.Rect.colliderect(self.rect,self.game.player_1.rect)
                if is_hit_left or abs((self.rect.x - self.game.player_1.player_pos[0]))<200:
                    self.game.player_1.knock_back_velocity_l = 10
                    self.game.player_1.upward_acceleration = True
                    self.game.player_1.player_health -= 1











        if self.bounce_counter >160 or self.rect.y > self.game.info.current_h - (self.game.info.current_h * 0.038) :
            self.velocity = 0
            self.bomb_acceleration = 0

            self.velocity_h = 0
            if self.rect.y > self.game.info.current_h - (self.game.info.current_h * 0.07):
                self.rect.y = self.game.info.current_h - (self.game.info.current_h * 0.065)


        #red flashing and self kill for bombs
        if self.bomb_acceleration == 0 and self.bounce_counter >180 and self.bounce_counter <300:
            if self.bounce_counter%20 == 0 or self.bounce_counter%40 == 0 :
                self.game.screen.blit(self.image_red,(self.rect.x,self.rect.y))
        elif self.bomb_acceleration == 0 and self.bounce_counter >300 and self.bounce_counter <400:
            if self.bounce_counter%5 == 0:
                self.game.screen.blit(self.image_red,(self.rect.x,self.rect.y))
        elif self.bomb_acceleration == 0 and self.bounce_counter >400:
            self.explosion_counter_counter += 1
            if self.explosion_counter_counter % 1 == 0:
                self.explosion_counter += 1


            self.game.screen.blit(self.game.explosions[self.explosion_counter], (self.rect.x-30, self.rect.y - 45))
            if self.explosion_counter > 8:
                self.kill()





        if self.rect.x < -5 or self.rect.x > self.game.info.current_w-30:
            self.velocity_h = -self.velocity_h

        if self.velocity > 0 and self.rect.colliderect(self.game.dumpster.rect):
            if self.rect.y < self.game.info.current_h * 0.8:
                if self.rect.centerx > self.game.dumpster.rect.left + 25 and self.rect.centerx < self.game.dumpster.rect.right-25:
                    if self.game.dumpster.collected < 31:
                        self.kill()
                        self.game.dumpster.collected +=1

        if (60.7 < self.game.difficulty_timer < 60.8) and self.game.difficulty_timer > 0:
            self.velocity_max +=5
            self.velocity_min +=5

        collide = pygame.Rect.colliderect(self.game.player_1.rect,self.rect)
        if collide and self.velocity_h <=0 and self.game.player_1.shield:
            self.velocity_h = -(self.velocity_h + 1)

        elif collide and self.velocity_h > 0 and self.game.player_1.shield_flipped:
            self.velocity_h = -(self.velocity_h + 1)





















