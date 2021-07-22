import pygame, math, random, os
import scripts.particles as particles
import scripts.sparks as sparks
import scripts.projectiles as projectiles

# this script will be different for every game
'''
------------------------------------------------------------- level manager -------------------------------------
'''
class Level_Manager():
    def __init__(self,particles_manager,sparks_manager,projectiles_manager):
        self.particles_manager = particles_manager
        self.sparks_manager = sparks_manager
        self.projectiles_manager = projectiles_manager
        # make sure starting point for each level is high off the ground because when player respawns the ground might not be rendered
        self.level_path = os.getcwd() + r'\data\files\json\levels' + '/'
        # for events and text the initiation in dependent on a 0,1,2 system 0 - haven't started, 1 - in progress, 2 - stop
        self.levels_data = {
                # path name for level
                'level_1_name' : self.level_path + 'level_1.json',
                # player pos at beginning of game
                'level_1_pos' :  [230,200],
                # if the level has bounds
                'level_1_bounds': True,
                # key[vaule] = type of text, bolliean to display ,text,loc of start and stop, offset for right movement for text
                # for type of text title = mid display and large and large font size, pos = the text is initiated by player loc,
                # bubble = display near player and small font size, achieve = (achievement) when a specific part of a level is completed
                # # key[vaule] = type of event, bolliean to display ,text,loc of start, is it a continuation event, freeze frame
                # for type of event pos = the text is initiated by player loc, achieve = (achievement) when a specific part of a level is completed
                'level_1_text_1':['title_pos',1,'use arrowkeys to move and space bar to jump',[ [-1,0],[404,0] ], [False,0] ],
                'level_1_event_1':['projectile_pos',0,[480,0],False,True],
                'level_1_text_2':['title_pos',0,'use arrowkeys and f key to faze',[ [480,0,0],[590,0] ], [False,0] ],
                'level_2_name' : self.level_path + 'level_2.json',
                'level_2_pos' :  [230,200],
                'level_3_name' : self.level_path + 'level_3.json',
                'level_3_pos' :  [230,200],
                    }
        self.level = 1
    '''
    ---------------------------------------------- reset ----------------------------------------------------
    '''
    # reset level data
    def reset(self):
        # reset event and text
        for key in self.levels_data:
            if int(key.split('_')[1]) == self.level:
                if key.split('_')[2] == 'event':
                    self.levels_data[key][1] = 0
                if key.split('_')[2] == 'text':
                    self.levels_data[key][1] = 0
    '''

    '''
    # get player pos
    def get_pos(self):
        return self.levels_data[f'level_{self.level}_pos'].copy()


    '''
    --------------------------------------------------- bounds -----------------------------------------------------
    '''
    def bounds(self,tile_map,TILE_SIZE,display,scroll):
        if self.levels_data[f'level_{self.level}_bounds']:
            # for left chose the min between scroll[0] and tile_map.left because tile_map.right will most of the time be signifcantly greater
            # for right the max between scroll[0] and tile_map.right because tile_map.left will most of the time be signifcantly smaller
            # same idea applies to y axis
            scroll[0] =  max(tile_map.left * TILE_SIZE, min(tile_map.right * TILE_SIZE - display.get_width() - TILE_SIZE ,scroll[0]))
            scroll[1] =  max(tile_map.up * TILE_SIZE, min(tile_map.down * TILE_SIZE - display.get_height() - TILE_SIZE ,scroll[1]))
            return scroll

    '''
    ----------------------------------------------------- event manager -------------------------------------------------------
    '''
    def events(self,player,scroll,display):
        for key in self.levels_data:
            if int(key.split('_')[1]) == self.level:
                if key.split('_')[2] == 'event':
                    if self.levels_data[key][0].split('_')[0] == 'projectile':
                        #projectile_events
                        # projectiles determined by pos of player
                        if self.levels_data[key][0].split('_')[1] == 'pos':
                            # if player is in front of set loc and the event hasn't started
                            if player.pos[0] > self.levels_data[key][2][0] and self.levels_data[key][1] == 0:
                                # set event to true
                                self.levels_data[key][1] = 1
                        if self.levels_data[key][1] == 1:
                            for i in range(27):
                                self.projectiles_manager.new('img_0', (display.get_width() + scroll[0], display.get_height()  * i // 17 -100 + scroll[1]),
                                                                           (-1, 0), random.random(), 'enemy',(50,22,20))
                            # if event only happens once
                            if self.levels_data[key][3] == False:
                                self.levels_data[key][1] = 2
                            # if event causes freeze frame
                            if self.levels_data[key][3] == True:
                                pass
    '''
    ----------------------------------------------------- message manager -------------------------------------------------------
    '''
    def messages(self,player,scroll,display):
        for key in self.levels_data:
            if int(key.split('_')[1]) == self.level:
                if key.split('_')[2] == 'text':
                    # messages that are title type
                    if self.levels_data[key][0].split('_')[0] == 'title':
                        # messages that are determined on pos of player
                        if self.levels_data[key][0].split('_')[1] == 'pos':
                            if player.pos[0] > self.levels_data[key][3][0][0] and self.levels_data[key][1] == 0:
                                self.levels_data[key][1] = 1
                            if player.pos[0] > self.levels_data[key][3][1][0] and self.levels_data[key][1] == 1:
                                self.levels_data[key][1] = 2
