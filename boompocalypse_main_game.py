import pygame
import sys
import random
import os
from os import listdir
from Scripts.enemies import Spaceship
from Scripts.enemies import Bomb
from Scripts.enemies import NuclearBomb
from Scripts.enemies import Missile
from Scripts.enemies import AlienFighter
from Scripts.enemies import Robot_Mech
from Scripts.utilities import load_images,Buttons
from Scripts.player import Player
from Scripts.player import Dumpster
from Scripts.player import TrashTruck









class Startscreen:
    def __init__(self):
        self.start_screen_run = True
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
        self.info = pygame.display.Info()
        self.screen_width = self.info.current_w
        self.screen_height = self.info.current_h
        self.mouse_pos = pygame.mouse.get_pos()

        self.bg = pygame.image.load('images/Start_screen_bg.png')
        self.bg = pygame.transform.scale(self.bg,(self.screen_width,self.screen_height))
        self.truck = pygame.image.load('images/trashtruck_start.png')
        self.truck = pygame.transform.scale(self.truck,(450,219))
        self.title_image = pygame.image.load('images/Text/Boompocalypse.png')
        self.title_image = pygame.transform.scale(self.title_image,(900,150))

        self.hazmatt_counter = 0
        self.hazmatt_counter_counter = 0
        self.hazmatt_rand = 0



        pygame.mixer.init()
        pygame.mixer.music.load("Audio/permafrost.mp3")
        pygame.mixer.music.play(-1, 0.0)

        self.hazmatt_cliff = []
        load_images('images/hazmatt_cliff/', '.png', self.hazmatt_cliff)
        self.hazmatt_cliff = [pygame.transform.scale(x, (80, 100)) for x in self.hazmatt_cliff]


        self.start_button = Buttons(self,200,600,pygame.image.load('images/Buttons/start_button.png'),0,True)
        self.title_button = Buttons(self,400,150,self.title_image,200,True)


        self.button_group = pygame.sprite.Group()
        self.button_group.add(self.start_button)
        self.button_group.add(self.title_button)


    def run(self):
        #self.screen.fill((156, 240, 137))



        while self.start_screen_run:



            #self.screen.fill((156, 240, 137))

            self.mouse_pos = pygame.mouse.get_pos()
            print(self.start_button.hover)


            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.hover:
                        self.start_screen_run = False



            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.truck,(1100,550))





            self.start_button.rect.centerx += 2
            if self.start_button.rect.centerx > self.screen_width + 100:
                self.start_button.rect.centerx = -100

            self.start_button.alpha += self.start_button.alpha_velocity
            self.start_button.image.set_alpha(self.start_button.alpha)

            if self.start_button.alpha > 120:
                self.start_button.alpha_velocity *= -1
            if self.start_button.alpha < 0:
                self.start_button.alpha_velocity *= -1

            self.title_button.alpha += self.title_button.alpha_velocity
            self.title_button.image.set_alpha(self.title_button.alpha)

            if self.title_button.alpha > 200:
                self.title_button.alpha_velocity *= -1
            if self.title_button.alpha < -50:
                self.title_button.alpha_velocity *= -1
            self.hazmatt_counter_counter +=1
            self.hazmatt_rand = random.randint(0,5000)
            if self.hazmatt_counter_counter % 4 == 0 and self.hazmatt_rand >4500:
                self.hazmatt_counter +=1
            if self.hazmatt_counter > 19:
                self.hazmatt_counter = 0
            self.screen.blit(self.hazmatt_cliff[self.hazmatt_counter],(1090,590))
            self.button_group.draw(self.screen)
            self.start_button.update()
            self.title_button.update()


            pygame.display.update()





class Game:
    def __init__(self):
        #self.screen = pygame.display.set_mode((0,0),0,32)
        self.game_timer = 0
        self.difficulty_timer = 0
        self.main_game = True

        self.mech_active = True

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
        self.info = pygame.display.Info()
        self.screen_width = self.info.current_w
        self.screen_height = self.info.current_h

        self.player_left = False
        self.player_right = False
        self.laser_collide = False

        self.hazmatt_death = []
        load_images('images/death_ani/','.png',self.hazmatt_death)
        self.hazmatt_death = [pygame.transform.scale(x,(160,155)) for x in self.hazmatt_death]

        self.hazmatt_shield =[]
        load_images('images/riot_shield/','.png',self.hazmatt_shield)
        self.hazmatt_shield = [pygame.transform.scale(x, (120, 185)) for x in self.hazmatt_shield]

        self.hazmatt_shield_flipped = [pygame.transform.flip(x, True, False) for x in self.hazmatt_shield]
        self.hazmatt_shield_flipped = [pygame.transform.scale(x, (120, 185)) for x in self.hazmatt_shield_flipped]



        self.hazmatt_jump = []
        load_images('images/hazmatt_jump/','.png',self.hazmatt_jump)
        self.hazmatt_jump = [pygame.transform.scale(x, (85, 150)) for x in self.hazmatt_jump]

        self.hazmatt_jump_blue = []
        load_images('images/hazmatt_jump/', '.png', self.hazmatt_jump_blue)
        self.hazmatt_jump_blue = [pygame.transform.scale(x, (85, 150)) for x in self.hazmatt_jump_blue]

        self.hazmatt_jump_left = [pygame.transform.flip(x, True, False) for x in self.hazmatt_jump]
        self.hazmatt_jump_left_blue = [pygame.transform.flip(x, True, False) for x in self.hazmatt_jump_blue]

        self.robot_mech_idle = []
        load_images('images/robot_mech_idle/','.png',self.robot_mech_idle)
        self.robot_mech_idle = [pygame.transform.scale(x, (235, 300)) for x in self.robot_mech_idle]

        self.robot_mech_idle_flipped = [pygame.transform.flip(x, True, False) for x in self.robot_mech_idle]
        self.robot_mech_idle_flipped = [pygame.transform.scale(x, (235, 300)) for x in self.robot_mech_idle_flipped]

        self.robot_mech_walk = []
        load_images('images/robot_mech_walk/', '.png', self.robot_mech_walk)
        self.robot_mech_walk = [pygame.transform.scale(x, (235, 300)) for x in self.robot_mech_walk]

        self.robot_mech_walk_flipped = [pygame.transform.flip(x, True, False) for x in self.robot_mech_walk]
        self.robot_mech_walk_flipped = [pygame.transform.scale(x, (235, 300)) for x in self.robot_mech_walk_flipped]

        self.robot_mech_reverse = []
        load_images('images/robot_mech_reverse/', '.png', self.robot_mech_reverse)
        self.robot_mech_reverse = [pygame.transform.scale(x, (235, 300)) for x in self.robot_mech_reverse]

        self.robot_mech_reverse_flipped = [pygame.transform.flip(x, True, False) for x in self.robot_mech_reverse]
        self.robot_mech_reverse_flipped = [pygame.transform.scale(x, (235, 300)) for x in self.robot_mech_reverse_flipped]

        self.robot_mech_shoot = []
        load_images('images/robot_mech_shoot/','.png', self.robot_mech_shoot)
        self.robot_mech_shoot = [pygame.transform.scale(x, (235, 300)) for x in self.robot_mech_shoot]

        self.robot_mech_shoot_flipped = [pygame.transform.flip(x, True, False) for x in self.robot_mech_shoot]
        self.robot_mech_shoot_flipped = [pygame.transform.scale(x, (235, 300)) for x in self.robot_mech_shoot_flipped]

        self.muzzle_flash = pygame.image.load('images/muzzle_flash.png')
        self.muzzle_flash = pygame.transform.scale(self.muzzle_flash, (self.screen_width * 0.07835, self.screen_height * 0.05097))

        self.muzzle_flash_flipped = pygame.transform.flip(self.muzzle_flash,True,False)
        self.muzzle_flash_flipped = pygame.transform.scale(self.muzzle_flash_flipped,(self.screen_width * 0.07835, self.screen_height * 0.05097))

        self.robot_saw = []
        load_images('images/robot_saw/','.png', self.robot_saw)
        self.robot_saw = [pygame.transform.scale(x, (295, 300)) for x in self.robot_saw]

        self.robot_saw_flipped = [pygame.transform.flip(x, True, False) for x in self.robot_saw]
        self.robot_saw_flipped = [pygame.transform.scale(x, (295, 300)) for x in self.robot_saw_flipped]

        self.robot_fly = []
        load_images('images/robot_mech_fly/','.png',self.robot_fly)
        self.robot_fly = [pygame.transform.scale(x, (295, 300)) for x in self.robot_fly]

        self.robot_fly_flipped = [pygame.transform.flip(x, True, False) for x in self.robot_fly]
        self.robot_fly_flipped = [pygame.transform.scale(x, (295, 300)) for x in self.robot_fly_flipped]

        self.player_blood_saw = []
        load_images('images/saw_bleed/', '.png', self.player_blood_saw)
        self.player_blood_saw = [pygame.transform.scale(x, (105, 165)) for x in self.player_blood_saw]

        self.player_blood_saw_flipped = [pygame.transform.flip(x, True, False) for x in self.player_blood_saw]
        self.player_blood_saw_flipped = [pygame.transform.scale(x, (105, 165)) for x in self.player_blood_saw_flipped]


        #self.missile_ani = []
        #load_images('images/missile_ani/', '.png', self.missile_ani)
        #self.missile_ani = [pygame.transform.scale(x, (205, 50)) for x in self.missile_ani]

        #self.missile_ani_flipped = [pygame.transform.flip(x, True, False) for x in self.missile_ani]

















        self.boom_text_ani = []
        load_images('images/Text/boom_animation/','.png',self.boom_text_ani)

        self.spaceship_ani = []
        load_images('images/Spaceship_animations/','.png',self.spaceship_ani)

        self.trash_truck_move = []
        load_images('images/trash_truck/', '.png', self.trash_truck_move)
        self.trash_truck_move = [pygame.transform.scale(x, (self.screen_width *0.573, self.screen_height * 0.5208)) for x in self.trash_truck_move]


        self.trash_truck_move_flipped = [pygame.transform.flip(x, True, False) for x in self.trash_truck_move]



        self.hazmatt_push = []
        load_images('images/Hazmattpush/','.png',self.hazmatt_push)
        self.hazmatt_push = [pygame.transform.scale(x, (self.screen_width*0.06835, self.screen_height*0.19097)) for x in self.hazmatt_push]
        self.push = False
        self.push_right = False
        self.push_left = False

        self.hazmatt_push_flipped = [pygame.transform.flip(x, True, False) for x in self.hazmatt_push]
        self.hazmatt_push_flipped = [pygame.transform.scale(x, (self.screen_width*0.06835, self.screen_height*0.19097)) for x in self.hazmatt_push_flipped]

        self.hazmatt_load = []
        load_images('images/test_animations/','.png',self.hazmatt_load)
        self.hazmatt_load = [pygame.transform.scale(x, (self.screen_width*0.06835,self.screen_height*0.19097 )) for x in self.hazmatt_load]

        self.alien_fighter_left = []
        load_images('images/alien_fighter_left/','.png',self.alien_fighter_left)
        self.alien_fighter_left = [pygame.transform.scale(x, (self.screen_width*0.15835,self.screen_height*0.23097 )) for x in self.alien_fighter_left]

        self.alien_fighter_right = [pygame.transform.flip(x, True, False) for x in self.alien_fighter_left]
        self.alien_fighter_right = [pygame.transform.scale(x, (self.screen_width*0.15835,self.screen_height*0.23097 )) for x in self.alien_fighter_right]

        self.nuclear_bomb = []
        load_images('images/nuclear_bomb_ani/','.png',self.nuclear_bomb)
        self.nuclear_bomb = [pygame.transform.scale(x, (self.screen_width * 0.07835, self.screen_height * 0.13097)) for x in self.nuclear_bomb]

        self.nuclear_bomb_flipped = [pygame.transform.flip(x, True, False) for x in self.nuclear_bomb]
        self.nuclear_bomb_flipped = [pygame.transform.scale(x, (self.screen_width * 0.07835, self.screen_height * 0.13097)) for x in self.nuclear_bomb_flipped]

        self.blue_laser_impact = []
        load_images('images/blue_laser_impact/', '.png', self.blue_laser_impact)
        self.blue_laser_impact = [pygame.transform.scale(x, (self.screen_width * 0.05835, self.screen_height * 0.08097)) for x in self.blue_laser_impact]

        self.nuke_explode = []
        load_images('images/nuke_explosion/','.png',self.nuke_explode)
        self.nuke_explode = [pygame.transform.scale(x, (self.screen_width * 0.12835, self.screen_height * 0.18097)) for x in self.nuke_explode]


        self.hazmatt_counter = 0
        self.hazmatt_counter_counter = 0
        self.hazmatt_look = False
        self.hazmatt_look_timer = 0
        self.dumpster_empty_counter = 0
        self.bomb_freq = 175



        self.player_idle_load_1 = []
        load_images('images/HazMattIdle/','.png',self.player_idle_load_1)
        self.player_idle_load_1 = [pygame.transform.scale(x, (85, 165)) for x in self.player_idle_load_1]

        self.player_idle_load_1_red = []
        load_images('images/HazMattIdle/', '.png', self.player_idle_load_1_red)
        self.player_idle_load_1_red = [pygame.transform.scale(x, (85, 165)) for x in self.player_idle_load_1_red]

        self.player_ani_1 = []
        load_images('images/HazMattrun/','.png',self.player_ani_1)
        self.player_ani_1 = [pygame.transform.scale(x, (105, 165)) for x in self.player_ani_1]
        #for image in self.player_ani_1:
            #image.set_colorkey((0,0,0))

        self.player_ani_1_red = []
        load_images('images/HazMattrun/', '.png', self.player_ani_1_red)
        self.player_ani_1_red = [pygame.transform.scale(x, (105, 165)) for x in self.player_ani_1_red]

        self.player_ani_1_red_flipped = [pygame.transform.flip(x, True, False) for x in self.player_ani_1_red]
        self.player_ani_1_red_flipped = [pygame.transform.scale(x, (105, 165)) for x in self.player_ani_1_red_flipped]






        self.explosions = []
        load_images('images/explosion/','.png',self.explosions)
        self.explosions = [pygame.transform.scale(x, (120, 120)) for x in self.explosions]

        self.player_ani_1_flipped = [pygame.transform.flip(x, True, False) for x in self.player_ani_1]
        self.player_ani_1_flipped = [pygame.transform.scale(x, (105,165)) for x in self.player_ani_1_flipped]
        #for image in self.player_ani_1_flipped:
            #image.set_colorkey((0,0,0))

        #text objects

        self.you_ready = pygame.image.load('images/Text/you_ready.png')
        self.you_ready = pygame.transform.scale(self.you_ready,(650,160))
        self.you_ready_x = -800
        self.you_ready_y = 300


        self.then_lets = pygame.image.load('images/Text/then_lets.png')
        self.then_lets = pygame.transform.scale(self.then_lets, (650,160))
        self.then_lets_x = -800
        self.then_lets_y = 300

        self.boom_text = self.boom_text_ani[0]
        self.boom_text_counter = 0
        self.boom_text_counter_counter = 0
        self.boom_text = pygame.transform.scale(self.boom_text,(850,360))
        self.boom_text_x = 500
        self.boom_text_y = 150














        #self.screen = pygame.display.set_mode((1200,500), 32)
        self.mouse = pygame.mouse


        self.clock = pygame.time.Clock()
        self.ground = self.info.current_h - (self.info.current_h *0.12)

        #health bar

        self.health_bar = pygame.image.load('images/healthbar.png')
        self.health_bar_alpha = 255







        #dumpster

        self.dumpster = Dumpster(self,(self.screen_width * 0.325),self.ground)
        self.dumpster_group = pygame.sprite.Group()
        self.dumpster_group.add(self.dumpster)


        #new player
        self.player_1 = Player(self,[650,self.ground])
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player_1)


        self.player_velocity_y = 0
        self.upward_acceleration = False
        self.up_acceleration = 0
        self.jump_timer = 0
        self.bomb_counter = 0



        self.bg = pygame.image.load('images/apocobackground1.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.info.current_w,self.info.current_h))







        #Sprites and sprite groups

        self.spaceship = Spaceship(self,340, 240, 300, -110)
        self.spaceship_group = pygame.sprite.Group()
        self.spaceship_group.add(self.spaceship)

        self.alien_fighter = AlienFighter(self,self.screen_width + 200,200)
        self.alien_fighter_group = pygame.sprite.Group()
        self.alien_fighter_group.add(self.alien_fighter)

        self.robot_mech = Robot_Mech(self, -125, 728)
        self.robot_mech_group = pygame.sprite.Group()
        self.robot_mech_group.add(self.robot_mech)

        self.nuke_group = pygame.sprite.Group()

        self.bomb_group = pygame.sprite.Group()

        self.blue_laser_group = pygame.sprite.Group()

        self.missile_group = pygame.sprite.Group()

        # trash truck

        self.trash_truck = TrashTruck(self, -500, self.ground-152, 'Left')
        self.trash_truck_right = TrashTruck(self,self.screen_width+450, self.ground-152,'Right')
        self.trash_truck_group = pygame.sprite.Group()
        self.trash_truck_group.add(self.trash_truck)
        self.trash_truck_group.add(self.trash_truck_right)


    def make_game_harder(self):
        if (60.7 < self.difficulty_timer < 60.8)  and self.bomb_freq > 40 and self.difficulty_timer > 0:
            self.bomb_freq -=3
            #if abs(self.spaceship.velocity_h < 10) and 100 < self.spaceship.rect.centerx < 900:
                #self.spaceship.velocity_h *= 1.05







    def start_screen(self):
        self.starting_screen.run()
        if self.main_game:
            self.run()




    def run(self):

        pygame.mixer.init()
        pygame.mixer.music.load("Audio/Spook2(chosic.com).mp3")
        pygame.mixer.music.play(-1, 0.0)

        while self.main_game:
            self.mouse.set_visible(False)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if event.type == pygame.KEYDOWN and self.player_1.player_health > 0:

                    if event.key == pygame.K_RIGHT and not self.push_left and self.player_1.shield == False and not self.player_1.saw_blade:
                        if not self.player_1.saw_blade:
                            self.player_1.player_move_h[1] = True

                    if self.player_1.rect.centerx < self.dumpster.rect.left or self.player_1.rect.centerx > self.dumpster.rect.right:
                        if event.key == pygame.K_z and self.player_1.shield == False:
                            self.push = True
                    if event.key == pygame.K_x and pygame.Rect.colliderect(self.player_1.rect,self.dumpster.rect) and pygame.Rect.colliderect(self.dumpster.rect, self.trash_truck.rect) and self.dumpster.collected > 0 and self.player_1.shield == False:
                        self.trash_truck.loading = True
                    if event.key == pygame.K_x and pygame.Rect.colliderect(self.player_1.rect,self.dumpster.rect) and pygame.Rect.colliderect(self.dumpster.rect, self.trash_truck_right.rect) and self.dumpster.collected > 0 and self.player_1.shield == False:
                        self.trash_truck.loading = True

                    if event.key == pygame.K_LEFT and not self.push_right and self.player_1.shield == False and not self.player_1.saw_blade:
                        if not self.player_1.saw_blade:
                            self.player_1.player_move_h[0] = True


                    if event.key == pygame.K_a and event.key == pygame.K_LEFT:
                        self.player_1.shield_flipped = True

                    if event.key == pygame.K_SPACE and self.player_1.shield == False:
                        if self.player_1.player_pos[1] == self.ground - 80:
                            self.player_1.upward_acceleration = True

                    if event.key == pygame.K_a and self.player_1.player_pos[1] == self.ground - 80:
                        self.player_1.shield = True







                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player_1.player_move_h[1] = False
                        self.player_1.player_run_counter = 0

                    if event.key == pygame.K_z:
                        self.push = False

                    if event.key == pygame.K_x:
                        self.trash_truck.loading = False
                        self.trash_truck.loading_time = 0

                    if event.key == pygame.K_LEFT:
                        self.player_1.player_move_h[0] = False
                        self.player_1.player_run_counter = 0

                    if event.key == pygame.K_a:
                        self.player_1.shield = False
                        self.player_1.shield_flipped = False
                        self.player_1.player_shield_counter = 0






            self.screen.blit(self.bg, (0, 0))




            #start words
            if self.game_timer <8:
                self.screen.blit(self.you_ready,(self.you_ready_x,self.you_ready_y))
            if self.game_timer > 2:
                self.you_ready_x +=50
            if self.game_timer < 5:
                if self.you_ready_x > 450:
                    self.you_ready_x = 450
            if self.game_timer > 5 and self.game_timer < 8:
                self.you_ready_y -=5

            if self.game_timer > 6 and self.game_timer < 7.5:
                self.screen.blit(self.then_lets,(self.then_lets_x,self.then_lets_y))
                self.then_lets_x += 50
                if self.then_lets_x > 500:
                    self.then_lets_x = 500
            if self.game_timer > 7:
                self.screen.blit(self.boom_text,(self.boom_text_x,self.boom_text_y))
                self.boom_text = self.boom_text_ani[self.boom_text_counter]
                self.boom_text_counter_counter+=1.5
                if self.boom_text_counter_counter % 3 == 0:
                    self.boom_text_counter +=1
            if self.boom_text_counter >26:
                self.boom_text_counter = 26




            #health bar
            self.health_bar_alpha = self.player_1.player_health * (self.player_1.player_health/255)
            self.health_bar = pygame.transform.scale(self.health_bar, (180, 180))
            self.screen.blit(self.health_bar, (6, 6))
            self.health_bar.set_alpha(self.health_bar_alpha)
            if self.health_bar_alpha < 0:
                self.health_bar_alpha = 0





            self.dumpster_group.update()
            self.dumpster_group.draw(self.screen)

            self.trash_truck_group.draw(self.screen)
            self.trash_truck_group.update()




            self.player_group.update()
            self.player_group.draw(self.screen)
            self.laser_collide = pygame.sprite.groupcollide(self.player_group, self.blue_laser_group, False,False)



            self.bomb_group.draw(self.screen)
            self.bomb_group.update()

            self.nuke_group.update()
            self.nuke_group.draw(self.screen)


            self.blue_laser_group.draw(self.screen)
            self.blue_laser_group.update()




            self.bomb_counter = random.randint(0,5000)
            if self.bomb_counter%self.bomb_freq == 0 and self.game_timer > 10:
                self.bomb_group.add(self.spaceship.create_bomb())


            if self.alien_fighter.rect.centery == 200 and self.game_timer > 10 and self.alien_fighter.nuke_rand%75 ==0:
                if self.alien_fighter.engage:
                    self.nuke_group.add(self.alien_fighter.create_nuke())

            if self.alien_fighter.rect.centery > 200 and self.alien_fighter.shoot_rand_rand%50 ==0:
                if self.alien_fighter.engage:
                    self.blue_laser_group.add(self.alien_fighter.shoot_laser())

            if self.robot_mech.in_flight and self.robot_mech.missile_counter > 900 and self.robot_mech.missile_counter < 930 and self.mech_active:
                if self.robot_mech.fly_cycles < 200:
                    self.missile_group.add(self.robot_mech.shoot_missile())



            #robot shooting behavior
            robot_player_collide = self.robot_mech.rect.colliderect(self.player_1.rect)
            if not robot_player_collide and self.robot_mech.in_flight == False and 0 < self.robot_mech.rect.centerx < self.screen_width:
                if self.bomb_counter % 20 == 0 and self.game_timer > 0:
                    if self.robot_mech.velocity_h == 0 and self.player_1.rect.centerx < self.robot_mech.rect.centerx:
                        self.blue_laser_group.add(self.robot_mech.shoot_laser(self, self.robot_mech.rect.centerx - 140, self.robot_mech.rect.centery + 20, False))
                        self.screen.blit(self.muzzle_flash_flipped,(self.robot_mech.rect.centerx - 190, self.robot_mech.rect.centery + 20))
                if self.bomb_counter % 22 == 0 and self.game_timer > 0:
                    if self.robot_mech.velocity_h == 0 and self.player_1.rect.centerx < self.robot_mech.rect.centerx:
                        self.blue_laser_group.add(self.robot_mech.shoot_laser(self, self.robot_mech.rect.centerx - 130, self.robot_mech.rect.centery + 50, False))
                        self.screen.blit(self.muzzle_flash_flipped,(self.robot_mech.rect.centerx - 230, self.robot_mech.rect.centery-5))

                if self.bomb_counter % 20 == 0 and self.game_timer > 0:
                    if self.robot_mech.velocity_h == 0 and self.player_1.rect.centerx > self.robot_mech.rect.centerx:
                        self.blue_laser_group.add(self.robot_mech.shoot_laser(self, self.robot_mech.rect.centerx + 110, self.robot_mech.rect.centery + 50, False))
                        self.screen.blit(self.muzzle_flash,(self.robot_mech.rect.centerx + 70, self.robot_mech.rect.centery + 20))
                if self.bomb_counter % 22 == 0 and self.game_timer > 0:
                    if self.robot_mech.velocity_h == 0 and self.player_1.rect.centerx > self.robot_mech.rect.centerx:
                        self.blue_laser_group.add(self.robot_mech.shoot_laser(self, self.robot_mech.rect.centerx + 130, self.robot_mech.rect.centery + 15, False))
                        self.screen.blit(self.muzzle_flash,(self.robot_mech.rect.centerx + 110, self.robot_mech.rect.centery-5))



            self.spaceship_group.draw(self.screen)
            self.spaceship_group.update()



            self.alien_fighter_group.draw(self.screen)
            self.alien_fighter.update()

            self.missile_group.draw(self.screen)
            self.missile_group.update()

            self.robot_mech_group.draw(self.screen)
            self.robot_mech.update()






            #loading progress bar
            if self.trash_truck.loading:
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.player_1.player_pos[0] - 40, self.player_1.player_pos[1] - 30, self.dumpster.collected * 4, 15))
                self.trash_truck.loading_time +=1
                self.dumpster_empty_counter += 1
                if self.dumpster_empty_counter%12 == 0:
                    self.dumpster.collected -= 1
                    #self.dumpster.emptied +=1
                    self.player_1.total_bombs_collected +=1

            if self.player_1.rect.centerx > self.screen_width/2:
                self.player_right = True
                self.player_left = False
            if self.player_1.rect.centerx < self.screen_width/2:
                self.player_right = False
                self.player_left = True



            self.make_game_harder()



            #and self.player_1.rect.centerx > self.dumpster.rect.centerx and self.player_1.rect.centerx < self.dumpster.rect.right and self.trash_truck.rect.centerx > 304:












            self.ticks = self.clock.tick(70)
            self.game_timer += 1/(self.ticks * 4)
            self.difficulty_timer +=1/(self.ticks * 4)
            if self.difficulty_timer > 61:
                self.difficulty_timer = 0

            print(self.player_1.total_bombs_collected)

            pygame.display.update()


start_screen = Startscreen()
game = Game()

start_screen.run()

if start_screen.start_screen_run == False:
    game.run()





