import pygame, random, math
# these imports are only used for rendering
import scripts.spritesheet_loader as spritesheet_loader
import scripts.core_fucs as core_fucs
from scripts.sine_wave_dat import x_varience as x_v


class Render_Map():
    def __init__(self, level_map,tile_size, map_path, tileset_path, display,levels_data):
        # tile size
        self.tile_size = tile_size
        # map path
        self.map_path = map_path
        # game map and tiles ------------- #
        self.spritesheets, self.offset_dat = spritesheet_loader.load_spritesheets(tileset_path)
        self.level_map = level_map
        self.level_map.load_map(map_path)
        # -------------------------------- #
        # display
        self.display = display
        # all objects that need to be rendered in the middle of ground and decroations
        self.mid_render = []
        # all collisions with player
        self.player_collisions = []
        # all conditions for tiles that need particle physics or projectiles ect
        self.conditions = []
        # timer for game
        self.game_time = 0
        # camera scroll
        self.scroll = [0,0]
        # rendering text vars ------------------ #
        # level data for text rendering
        self.levels_data = levels_data


    '''
    --------------------------------------------------- main self.display -------------------------------------------
    '''

    # self.displays all visible tiles according to camera or scroll ------ #
    # also renders objects in between ground and other tiles if needed -- #
    def render_visible(self, scroll):
        self.scroll = scroll
        self.game_time += 1
        self.player_collisions = []
        # visible tiles list
        render_list = self.level_map.get_visible(scroll)

        # Render Tiles Not Ground --------------------------------------------------------------------- #
        for layer_dat in render_list:
            layer = layer_dat[1]
            for tile in layer['grid_tiles']:
                # tile is a key (0,0) for a specific tile ------------------ #
                tile = layer['grid_tiles'][tile]
                if tile['type_dat'][0] != 'ground':
                    offset = [0, 0]
                    # find offset through too much iteration (view json file) ----------- #
                    if tile['type_dat'][0] in self.offset_dat:
                        tile_id = str(tile['type_dat'][1]) + ';' + str(tile['type_dat'][2])
                        if tile_id in self.offset_dat[tile['type_dat'][0]]:
                            if 'tile_offset' in self.offset_dat[tile['type_dat'][0]][tile_id]:
                                offset = self.offset_dat[tile['type_dat'][0]][tile_id]['tile_offset'][0], \
                                         self.offset_dat[tile['type_dat'][0]][tile_id]['tile_offset'][1]
                    # tile is a the data from the specific key (tile) ------------------ #
                    img = spritesheet_loader.get_img(self.spritesheets, tile['type_dat'])
                    self.display.blit(img,
                                      (math.floor(tile['render_pos'][0] - scroll[0] + offset[0]),
                                       math.floor(tile['render_pos'][1] - scroll[1] + offset[1])))

                for condition_dat in self.conditions:
                    if tile['type_dat'][0] == condition_dat[0]:
                        self.find_condition(condition_dat, tile, offset)

        # if layers before ground have been parsed then render anything in middle objects then other tiles
        if self.mid_render != []:
            for obj_dat in self.mid_render:
                obj = obj_dat[0]
                obj.render(self.display, self.scroll)

        # Render Tiles Ground --------------------------------------------------------------------- #
        for layer_dat in render_list:
            layer = layer_dat[1]
            for tile in layer['grid_tiles']:
                # tile is a key (0,0) for a specific tile ------------------ #
                tile = layer['grid_tiles'][tile]
                if tile['type_dat'][0] == 'ground':
                    offset = [0, 0]
                    # find offset through too much iteration (view json file) ----------- #
                    if tile['type_dat'][0] in self.offset_dat:
                        tile_id = str(tile['type_dat'][1]) + ';' + str(tile['type_dat'][2])
                        if tile_id in self.offset_dat[tile['type_dat'][0]]:
                            if 'tile_offset' in self.offset_dat[tile['type_dat'][0]][tile_id]:
                                offset = self.offset_dat[tile['type_dat'][0]][tile_id]['tile_offset'][0], \
                                         self.offset_dat[tile['type_dat'][0]][tile_id]['tile_offset'][1]
                    # add ground to collisions
                    self.player_collisions.append(
                        pygame.rect.Rect(tile['render_pos'][0], tile['render_pos'][1], self.tile_size, self.tile_size))
                    # tile is a the data from the specific key (tile) ------------------ #
                    img = spritesheet_loader.get_img(self.spritesheets, tile['type_dat'])
                    self.display.blit(img,
                                      (math.floor(tile['render_pos'][0] - scroll[0] + offset[0]),
                                       math.floor(tile['render_pos'][1] - scroll[1] + offset[1])))


    '''
    ------------------------------------ middle render ---------------------------------------
    '''

    # add a object to blit in middle of ground and other tiles ---- #
    def add_mid_render(self, obj):
        self.mid_render.append([obj])

    def remove_mid_render(self, object):
        for i, obj in sorted(enumerate(self.mid_render), reverse=True):
            if obj[0] == object:
                self.mid_render.pop(i)

    '''
    ------------------------------------------- conditions --------------------------------------------
    '''

    # add condition for certain tile ex - torches and give condition like particles and glow
    def add_condition(self, tile_name, function_name, function_assets=None):
        if [tile_name, function_name, function_assets] in self.conditions:
            pass
        else:
            self.conditions.append([tile_name, function_name, function_assets])

    # render options for certain tiles -------------- #
    def find_condition(self, condition_dat, tile, offset):
        assets = condition_dat[2]
        # condition data should be [  tile_name,particle,particle_manager object  ]
        if condition_dat[1] == 'particle':
            self.create_particle(assets, tile, offset)
        # condition data should be [ tile_name,particle,num of glows ]
        if condition_dat[1] == 'glow':
            surfs = self.create_glow(tile, assets)
            self.render_glow(surfs, tile, offset)

    '''
    --------------------------------------- condition functions --------------------------------------------------
    '''

    # particles ----------------------------------------------- #

    # create particle
    def create_particle(self, assets, tile, offset):
        particle_manager = assets
        # particles
        if random.randint(1, 6) == 1:
            # create particles
            particle_manager.new('green_light', (
                tile['render_pos'][0] + offset[0] + 1, tile['render_pos'][1] + offset[1] - 2),
                                 (random.randint(95, 105) / 100 - 1, random.randint(100, 150) / -1000),
                                 3 + random.randint(0, 20) / 10, .1)

    # --------------------------------------------------------------- #

    # glows --------------------------------------------------------- #

    # create glow surf
    def create_glow(self, tile, num_glows):
        surf_l = []
        # torch glow
        torch_sin = math.sin((tile['render_pos'][1] % 200) / 300 * self.game_time * .01)
        for i in range(num_glows):
            surf = core_fucs.circle_surf((15 * (i + 1)) + (torch_sin + 3) * (2.5 + (i + 1)),
                                         (9 + torch_sin, 18 + torch_sin, 12 + torch_sin))
            surf_l.append(surf)
        return surf_l

    # render glow
    # rendering is only in render module because it doesnt have its own
    def render_glow(self, surfs, tile, offset):
        # render glow
        for surf in surfs:
            core_fucs.blit_center_special(self.display, surf, (tile['render_pos'][0] + offset[0] + 8 - self.scroll[0],
                                                               tile['render_pos'][1] + offset[1] + 5 - self.scroll[1]))

    # ---------------------------------------------------------------- #

    '''
    ------------------------------------------------------- fog ---------------------------------------------
    '''

    def fog(self,type=None,color = (255,255,255),height = 16,waves = 6,amplitude = 4,sin_speed = [10,10],alpha = [True,55],scale = 2,sides = 2,stack = 2,offset = 6,x_scale=8):
        sin_range = waves * 6
        # offset for stacked
        offset = offset  * scale
        # vars ------------- #
        # points ------------ #
        # bottom left
        points = [[0,height]]
        # all points that make the sin wave
        sin_points = [[self.display.get_width() / sin_range  * (i + 1) + x_v(type,i,x_scale,self.game_time,self.scroll)
                          , height + math.sin((self.game_time + i * sin_speed[0]) / sin_speed[1]) * amplitude] for i in range(sin_range - 1)]

        max_y = sorted(sin_points[1])[-1] + offset * scale

        points += sin_points
        # bottom right,top right, top left
        points += [[self.display.get_width(),height], [self.display.get_width(), 0], [0, 0]]

        points = [[self.display.get_width() - p[0] ,p[1]* scale] for p in points]

        # blit on surf
        surf = pygame.surface.Surface((self.display.get_width(), max_y + 2))

        # edit surf
        pygame.draw.polygon(surf, color, points)
        surf.set_colorkey((0, 0, 0))
        if alpha[0]:
            surf.set_alpha(alpha[1])
        # blit surf top screen
        if sides > 1:
            if stack > 1:
                self.display.blit(pygame.transform.flip(surf.copy(), True, False), (0, -offset))
            self.display.blit(surf.copy(), (0, 0))
            # blit surf bottom screen
            if stack > 1:
                self.display.blit(pygame.transform.flip(surf.copy(), True, True), (0, self.display.get_height() - max_y + offset))
            self.display.blit(pygame.transform.flip(surf.copy(), False, True), (0, self.display.get_height() - max_y))

        # blit surf left screen
        side_surf = pygame.transform.scale(pygame.transform.rotate(surf.copy(), 90),(int(max_y), self.display.get_height()))

        if sides > 2:
            if stack > 1:
                self.display.blit(pygame.transform.flip(side_surf.copy(), False, True), (-offset, 0))
            self.display.blit(side_surf.copy(), (0, 0))
            # blit surf right screen
            if stack > 1:
                self.display.blit(pygame.transform.flip(side_surf.copy(), True, True),(self.display.get_width() - max_y + offset, 0))
            self.display.blit(pygame.transform.flip(side_surf.copy(), True, False), (self.display.get_width() - max_y, 0))


    '''
    ------------------------------------------------------ render text --------------------------------------------------------------
    '''
    def text_title_pos(self,fonts,level,player):
        # render level text
        for key in self.levels_data:
            # display text
            if int(key.split('_')[1]) == level:
                if key.split('_')[2] == 'text':
                    # if text needs to be displayed
                    if self.levels_data[key][1] == 1:
                        # determine right movement for text
                        if self.levels_data[key][3][1][0] - player.pos[0] < 40:
                            self.levels_data[key][4][0] = True
                        if self.levels_data[key][4][0]:
                            self.levels_data[key][4][1] += 7
                        offset_x = self.levels_data[key][4][1]
                        # determine if str need more than one line
                        if len(self.levels_data[key][2]) > 20:
                            text_l = []
                            num_lines = len(self.levels_data[key][2])//20
                            temp_text_l = self.levels_data[key][2].split(' ')
                            num_text = len(temp_text_l)
                            for i in range(num_lines):
                                j = num_text//num_lines
                                temp_list = temp_text_l[:j]
                                if len(temp_text_l) < j * 2:
                                    temp_list = temp_text_l
                                list = ''
                                for word in temp_list:
                                    list += word + ' '
                                text_l.append(list)
                                temp_text_l = temp_text_l[j:]
                            for i, text in enumerate(text_l):
                                pos = (self.display.get_width()//2 - fonts[0].get_size(text) // 2 + offset_x,self.display.get_height()//2 - (len(text_l) * 20) + (i * 15) )
                                for i, font in enumerate(fonts):
                                    font.render(text,self.display,(pos[0],pos[1]+(i-1)))
                        else:
                            pos = (self.display.get_width()//2 - fonts[0].get_size(self.levels_data[key][2]) // 2 + offset_x,self.display.get_height()//2)
                            for i, font in enumerate(fonts):
                                font.render(text,self.display,(pos[0],pos[1]+(i-1)))

                    else:
                        self.levels_data[key][4][0] = False
                        self.levels_data[key][4][1] = 0
