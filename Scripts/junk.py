"""if self.player_run_counter > 24:
                            self.player_run_counter = 0
                        if self.player_idle_counter > 20:
                            self.player_idle_counter = 0"""


"""if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    if event.key == pygame.K_RIGHT:
                        self.player_move_h[1] = True

                    if event.key == pygame.K_LEFT:
                        self.player_move_h[0] = True

                    if event.key == pygame.K_SPACE:
                        if self.player_pos[1] == self.ground:
                            self.upward_acceleration = True"""


""" if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player_move_h[1] = False
                    if event.key == pygame.K_LEFT:
                        self.player_move_h[0] = False"""


"""if self.player_move_h[1]:

                self.run_counter_counter += 1
                if self.run_counter_counter % 2 == 0:
                    self.player_run_counter += 1

                self.screen.blit(self.player_scaled[self.player_run_counter], self.player_pos)

            elif self.player_move_h[0]:
                self.run_counter_counter += 1
                if self.run_counter_counter % 2 == 0:
                    self.player_run_counter += 1


                self.screen.blit(self.player_scaled_flipped[self.player_run_counter],self.player_pos)


            else:
                self.idle_counter_counter += 1
                if self.idle_counter_counter % 8 == 0:
                    self.player_idle_counter += 1
                self.screen.blit(self.player_idle_scaled[self.player_idle_counter], self.player_pos)

                #self.screen.blit(self.player_idle_load_1[self.player_idle_counter], (500,500))

            self.player_pos[0] += (self.player_move_h[1] - self.player_move_h[0]) * 6.5


            #vertical physics

            self.player_pos[1] -= self.player_velocity_y
            if self.upward_acceleration:
                self.player_velocity_y = 10
                self.player_velocity_y -= self.up_acceleration
                self.up_acceleration += 0.4
                self.jump_timer += 1
            if self.jump_timer > 50:
                self.jump_timer = 0
                self.upward_acceleration = False
                self.up_acceleration = 0"""


"""self.player = pygame.image.load('images/run/0.png')
        self.player_idle_load = [pygame.image.load('images/idle/00.png'), pygame.image.load('images/idle/01.png'),
                                 pygame.image.load('images/idle/02.png'), pygame.image.load('images/idle/03.png'),
                                 pygame.image.load('images/idle/04.png'), pygame.image.load('images/idle/05.png'),
                                 pygame.image.load('images/idle/06.png'), pygame.image.load('images/idle/07.png'),
                                 pygame.image.load('images/idle/08.png'), pygame.image.load('images/idle/09.png'),
                                 pygame.image.load('images/idle/10.png'), pygame.image.load('images/idle/11.png'),
                                 pygame.image.load('images/idle/12.png'), pygame.image.load('images/idle/13.png'),
                                 pygame.image.load('images/idle/14.png'), pygame.image.load('images/idle/15.png'),
                                 pygame.image.load('images/idle/16.png'), pygame.image.load('images/idle/17.png'),
                                 pygame.image.load('images/idle/18.png'), pygame.image.load('images/idle/19.png'),
                                 pygame.image.load('images/idle/20.png'), pygame.image.load('images/idle/21.png')]
        self.player_ani = [pygame.image.load('images/run/0.png'), pygame.image.load('images/run/0.png'),
                           pygame.image.load('images/run/0.png'), pygame.image.load('images/run/1.png'),
                           pygame.image.load('images/run/1.png'), pygame.image.load('images/run/1.png'),
                           pygame.image.load('images/run/2.png'), pygame.image.load('images/run/2.png'),
                           pygame.image.load('images/run/2.png'), pygame.image.load('images/run/3.png'),
                           pygame.image.load('images/run/3.png'), pygame.image.load('images/run/3.png'),
                           pygame.image.load('images/run/3.png'), pygame.image.load('images/run/4.png'),
                           pygame.image.load('images/run/4.png'), pygame.image.load('images/run/4.png'),
                           pygame.image.load('images/run/5.png'), pygame.image.load('images/run/5.png'),
                           pygame.image.load('images/run/5.png'), pygame.image.load('images/run/6.png'),
                           pygame.image.load('images/run/6.png'), pygame.image.load('images/run/6.png'),
                           pygame.image.load('images/run/7.png'), pygame.image.load('images/run/7.png'),
                           pygame.image.load('images/run/7.png'), pygame.image.load('images/run/7.png')]"""



        """self.player_scaled = [pygame.transform.scale(x, (84, 84)) for x in self.player_ani]
        self.player_scaled_flipped = [pygame.transform.flip(x, True, False) for x in self.player_ani]
        self.player_scaled_flipped = [pygame.transform.scale(x, (84, 84)) for x in self.player_scaled_flipped]
        for i in self.player_scaled:
            i.set_colorkey((0,0,0))
        for i in self.player_scaled_flipped:
            i.set_colorkey((0,0,0))

        self.player_idle_scaled = [pygame.transform.scale(x, (84, 84)) for x in self.player_idle_load]

        self.player_move_v = [False, False]
        self.player_move_h = [False, False]

        self.player_pos = [600, self.ground]
        self.player_run_counter = 0
        self.run_counter_counter = 0

        self.player_idle_counter = 0
        #self.idle_counter_counter = 0

if self.player_pos[1] > self.ground:
    self.player_pos[1] = self.ground"""










""" if self.side == 'Right':
            self.velocity = 4

            if self.right_rand_appear >1 and self.game.dumpster.collected >1 and self.truck_timer_right<400 and self.game.player_1.rect.centerx < self.game.screen_width/2: #and self.game.player_1.rect.centerx < self.game.screen_width/2:
                self.velocity = -4



            if self.rect.centerx < self.game.screen_width - 305:
                self.rect.centerx = self.game.screen_width - 305
            if self.rect.centerx == self.game.screen_width - 305:
                self.truck_timer_right +=1
            if self.truck_timer_right > 400:
                self.velcocity = -self.velocity

            if self.rect.centerx > self.game.screen_width + 450:
                self.rect.centerx = self.game.screen_width + 450
                self.truck_timer_right = 0


            if self.velocity < 0:
                self.ani_counter += 1
            elif self.velocity > 0:
                self.ani_counter -= 1
            if self.ani_counter > 14:
                self.ani_counter = 0
            if self.ani_counter < 0:
                self.ani_counter = 14
            if self.rect.centerx > self.game.screen_width - 305:
                self.image = self.game.trash_truck_move_flipped[self.ani_counter]
            else:
                self.image = self.game.trash_truck_move_flipped[0]"""














             """if self.truck_timer == 700 or self.loading_time > 400:
                self.velocity = -self.velocity
                self.loading_time = 0
                self.truck_timer = 0

            if self.rect.centerx < self.game.screen_width - 305:
                self.rect.centerx = self.game.screen_width - 305

            if self.rect.centerx > self.game.screen_width + 450:
                self.rect.centerx = self.game.screen_width + 450

            if self.rect.centerx > self.game.screen_width - 305:

                self.ani_counter_counter += 1
                if self.ani_counter_counter % 1 == 0:
                    if self.velocity < 0:
                        self.ani_counter += 1
                    elif self.velocity > 0:
                        self.ani_counter -= 1
                if self.ani_counter > 14:
                    self.ani_counter = 0
                if self.ani_counter < 0:
                    self.ani_counter = 14
                self.image = self.game.trash_truck_move_flipped[self.ani_counter]

            if self.rect.centerx < self.game.screen_width - 304:
                self.image = self.game.trash_truck_move_flipped[0]
                self.image = pygame.transform.scale(self.image, (880, 450))

            #if self.game.dumpster.dumpster_posx < self.rect.centerx + 375:
                #self.game.dumpster.dumpster_posx = self.rect.centerx + 375"""











