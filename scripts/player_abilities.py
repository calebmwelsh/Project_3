import pygame, math, random


class Abilities():
    def __init__(self,particles_manager,sparks_manager,projectiles_manager):
        # managers
        self.particles_manager = particles_manager
        self.sparks_manager = sparks_manager
        self.projectiles_manager = projectiles_manager
        # faze
        self.faze = False
        self.faze_initiation = False
        self.faze_counter = 0
        self.cooldown = 20
        self.faze_vel = [6,6]
        self.faze_acc = [.1,.1]
        self.faze_jurk = [.03,.03]

    '''
    ----------------------------------------------- reset -----------------------------------------------------
    '''
    def reset(self):
        self.faze = False
        self.faze_counter = 0
        self.cooldown = 20
        # reset physics
        self.faze_vel = [6,6]
        self.faze_acc = [.1,.1]
        self.faze_jurk = [.03,.03]

    '''
    -------------------------------------------------- faze ---------------------------------------------
    '''
    # initate faze including effects
    def faze_initialize(self,player):
        if self.faze_initiation:
            # increase image size
            player.scale[0] += 1
            player.scale[1] += 1
            # increase transparency
            player.opacity = 100
            # cause only upward fazes
            if player.vel[1] > 0:
                player.vel[1] = 0
            # turn graviity off during faze
            player.gravity_toggle = True
            '''
            ------------------------------------- sparks ----------------------------------------------------
            '''
            # create effects for faze animation
            # sparks
            # find offset and angle
            for i in range(60):
                # if player is moving in the x direction
                if player.vel[0] != 0:
                    # if player is moving right
                    if player.vel[0] > 0:
                        offset_x = 15
                        offset_y = 0
                        angle = math.radians(random.randint(130,220))
                    # if player is moving right
                    if player.vel[0] < 0:
                        offset_x = -15
                        offset_y = 0
                        angle = math.radians(random.randint(130,220) + 180)
                    # if player is moving right or left and up
                    if player.vel[1] < 0:
                        if player.vel[0] > 0:
                            offset_x = 7
                            offset_y = 7
                            angle = math.radians(random.randint(0,90) + 90)
                        if player.vel[0] < 0:
                            offset_x = -7
                            offset_y = 7
                            angle = math.radians(random.randint(0,90))
                if player.vel[0] == 0:
                    # player is in the air and not moving right or left
                    if player.air_timer > 2:
                        angle = math.radians(random.randint(40,140))
                        offset_x = 0
                        offset_y = 15
                    # player is not moving at all
                    if player.air_timer <= 2:
                        angle = math.radians(random.randint(40,140) + 180)
                        offset_x = 0
                        offset_y = -15
                self.sparks_spawn =  [player.center[0] - player.vel[0] - offset_x, player.center[1] - player.vel[1] + offset_y]
                speed = random.randint(70,150)/15 * .35
                # red (203,129,117)
                # green
                # yellow
                self.sparks_manager.new(self.sparks_spawn,angle,speed,5,(203,129,117),'s')

            '''
            ------------------------------------------- faze movement ----------------------------------------------
            '''
            # control faze movement in multiple directions
            # control faze movement in one direction
            if player.vel[0] != 0:
                if player.vel[1] < 0:
                    # reset player y vel so every faze is equal
                    player.vel[1] = 0
                    if player.vel[0] > 0:
                        # if player is moving up and to the right
                        self.faze_vel[0] =  self.faze_vel[0] * .90
                        self.faze_vel[1] = -self.faze_vel[1] * .90
                        self.faze_acc[0] =  self.faze_acc[0]
                        self.faze_acc[1] = -self.faze_acc[1]
                        self.faze_jurk[0] =  -self.faze_jurk[0]
                        self.faze_jurk[1] = self.faze_jurk[1]
                    elif player.vel[0] < 0:
                        # if player is moving up and to the left
                        self.faze_vel[0] = -self.faze_vel[0] * .90
                        self.faze_vel[1] = -self.faze_vel[1] * .90
                        self.faze_acc[0] =  -self.faze_acc[0]
                        self.faze_acc[1] = -self.faze_acc[1]
                        self.faze_jurk[0] =  self.faze_jurk[0]
                        self.faze_jurk[1] = self.faze_jurk[1]
                else:
                    # if player is moving left or right
                    if player.vel[0] > 0:
                        self.faze_vel[0] = self.faze_vel[0]
                        self.faze_acc[0] = self.faze_acc[0]
                        self.faze_jurk[0] = -self.faze_jurk[0]
                        self.faze_vel[1] = 0
                        self.faze_acc[1] = 0
                        self.faze_jurk[1] = 0
                    if player.vel[0] < 0:
                        self.faze_vel[0] = -self.faze_vel[0]
                        self.faze_acc[0] = -self.faze_acc[0]
                        self.faze_jurk[0] = self.faze_jurk[0]
                        self.faze_vel[1] = 0
                        self.faze_acc[1] = 0
                        self.faze_jurk[1] = 0
            else:
                # reset player y vel so every faze is equal
                player.vel[1] = 0
                # if player is in air but not moving left or right
                if player.air_timer > 3:
                    self.faze_vel[1] = -self.faze_vel[1]
                    self.faze_acc[1] = -self.faze_acc[1]
                    self.faze_jurk[1] =  self.faze_jurk[1]
                    self.faze_vel[0] = 0
                    self.faze_acc[0] = 0
                    self.faze_jurk[0] = 0
                # if player is stationary
                else:
                    self.faze_vel[0] = 0
                    self.faze_acc[0] = 0
                    self.faze_jurk[0] = 0
                    self.faze_vel[1] = 0
                    self.faze_acc[1] = 0
                    self.faze_jurk[1] = 0
    # faze physics and timer
    def faze_current(self,player):
        if self.faze:
            '''
            ------------------------------------- movement and scale -----------------------------------------------
            '''
            # increase player size
            if self.faze_counter // 3 == 0:
                player.scale[0] += 1
                player.scale[1] += 1
            # determine vel and acc
            self.faze_acc[0] += self.faze_jurk[0]
            self.faze_acc[1] += self.faze_jurk[1]
            self.faze_vel[0] += self.faze_acc[0]
            self.faze_vel[1] += self.faze_acc[1]
            # change player pos
            player.vel[0] = self.faze_vel[0]
            player.vel[1] = self.faze_vel[1]


            '''
            -------------------------------------------- faze counter ---------------------------------------------
            '''
            # increase faze counter
            self.faze_counter += 1
            # if faze is expired
            if self.faze_counter > 20:
                # reset player attributes
                player.scale[0] = 1
                player.scale[1] = 1
                player.opacity  = 255
                player.gravity_toggle = False
                player.vel[0] = 0
                player.vel[1] = 0
                # reset faze
                self.reset()
            # faze initiation is completed
            self.faze_initiation = False
    # update faze and cooldown
    def update_faze(self,player,display,scroll):
        '''
        ------------------------------------------- faze cooldown -------------------------------------------
        '''
        if self.cooldown > -1:
            self.cooldown -= 1
        if self.cooldown < 0:
            self.faze_initialize(player)
            self.faze_current(player)
        else:
            self.faze_initiation = False
            self.faze = False






            '''
            want to create lines on top and bottom of player when fazeing
            finish sparks to see if should be implemted
            make this code neater aka level manager
            '''


            '''
            ----------------------------------------------- pulse ------------------------------------------

            if self.faze_initiation:
                self.pulse_spawn = [player.center[0] - scroll[0],player.center[1] - scroll[1]]

            pygame.draw.circle(display,(203,129,117),self.pulse_spawn, self.faze_counter,2)
            '''

            '''
            start_pos = (player.center[0] - scroll[0] - player.vel[0] * 10,player.pos[1] - scroll[1] )
            end_pos = (player.center[0] - scroll[0] - player.vel[0] * 20, player.pos[1] - scroll[1])
            pygame.draw.line(display,(203,129,117),start_pos ,end_pos , 1)
            '''

            '''
            # sparks
            for i in range(9):
                spawn = (player.pos[0] - player.vel[0] * 6,player.pos[1])
                if player.vel[0] > 0:
                    angle_x = 180
                if player.vel[0] < 0:
                    angle_x = 0
                if player.vel[0] == 0:
                    angle_x = i * 20 + 90
                angle_y = i * 20 + 90
                speed = random.randint(70,150)/15 * .5
                vel = (math.cos(angle_x) * speed ,math.sin(angle_y) * speed)
                for i in range(3):
                    angle = math.radians(random.randint(110,250))
                    sparks_manager.new(spawn,angle + math.radians(random.randint(20,80) -40),speed,5 + random.randint(30,50)/10,(0, 0,0),'s')



            # create particle explosion
            for i in range(18):
                pos = (player.pos[0] - player.vel[0] * 6,player.pos[1])
                if player.vel[0] > 0:
                    angle_x = 180
                if player.vel[0] < 0:
                    angle_x = 0
                if player.vel[0] == 0:
                    angle_x = i * 10 + 90
                angle_y = i * 10 + 90
                speed = random.randint(70,150)/15 * .5
                vel = (math.cos(angle_x) * speed ,math.sin(angle_y) * speed)
                particles_manager.new('yellow_light',pos, vel,1 + random.randint(0, 20) / 10, .5)'''
