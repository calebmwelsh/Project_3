# Setup pygame/window ---------------------------------------- #
import pygame, sys, math, os
from pygame.locals import *
import spritesheet_loader
import chunker
import text
from core_fucs import *
from pathlib import Path

parent = os.path.dirname(__file__)
dir_path = Path(parent).parent.absolute()
os.chdir(dir_path)

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('tile_editor')

display_size = [600, 400]
display_scale = 2
particle_speed = 0.5
particle_duration = 1
particle_rate = 10
screen = pygame.display.set_mode((display_size[0] * display_scale, display_size[1] * display_scale), 0, 32)
display = pygame.Surface(display_size)

# vars ----------------------- #
scale = 2
tile_size = 17
editor_size = 1100
dis = editor_size // tile_size
# fonts
font = text.Font('data/font/font_image.png',(255,255,255))
# assets
spritesheets, offset_dat = spritesheet_loader.load_spritesheets(('data/images/tilesets'))
level_map = chunker.TileMap([tile_size,tile_size], display_size)
ground_tile_config = json.loads(read_f('data/files/json/tile_editor/ground_auto_config.json'))
background_tile_config = json.loads(read_f('data/files/json/tile_editor/background_auto_config.json'))

# functions ------------------------------------------------------------------- #
def get_selection_pos_list(selection_points):
    selection_points = rect_corners(selection_points)
    start = [int(round(selection_points[0][0] / tile_size - 0.5, 0)),
             int((round(selection_points[0][1] / tile_size - 0.5, 0)))]
    end = [int(round(selection_points[1][0] / tile_size - 0.5, 0)),
           int((round(selection_points[1][1] / tile_size - 0.5, 0)))]
    return points_between_2d([start, end])


def flood_fill(pos, level_map, sel_sheet, layer):
    remaining_tiles = [pos]
    tile_dat = [sel_sheet,len(spritesheets[sel_sheet])-1,0]
    counter = 0
    while remaining_tiles != []:
        remaining_tiles_c = remaining_tiles.copy()
        remaining_tiles = []
        for point in remaining_tiles_c:
            level_map.add_tile(tile_dat.copy(), point, layer)
            bordering_tiles = [[point[0] + 1, point[1]],
                               [point[0] - 1, point[1]],
                               [point[0], point[1] + 1],
                               [point[0], point[1] - 1]]
            for b_tile in bordering_tiles:
                if not level_map.get_tile(b_tile, layer):
                    if b_tile not in remaining_tiles:
                        remaining_tiles.append(b_tile)
        counter += 1
        if counter > 100:
            return True
    return False


def auto_tile(selection_points, level_map, layer, selected_spritesheet):
    # the check list in the auto config test each tile for each pos up down right left..
    # then if that is in the border tile then switches to that tile
    global spritesheets, ground_tile_config,background_tile_config
    if selected_spritesheet != 'ground':
        tile_config = background_tile_config
    else:
        tile_config = ground_tile_config
    tile_list = selection_points
    tile_index_list = [int(b['tile'][0]) for b in tile_config['borders']]
    if len(spritesheets[selected_spritesheet]) >= max(tile_index_list) + 1:
        for tile in tile_list:
            # returns none if there is no tile in loc or tile info starting with pos as key
            tile_dat = level_map.get_tile(tile, layer)
            if tile_dat:
                found_locs = []
                for loc in tile_config['check_list']:
                    # checks left right up down from tile
                    search_loc = [loc[0] + tile[0], loc[1] + tile[1]]
                    # if tile is found append
                    if level_map.get_tile(search_loc, layer):
                        found_locs.append(loc)
                for tile_setting in tile_config['borders']:
                    # if the loc in check list that the tile corresponds to is equal to the...
                    # specific tile then switches it
                    if sorted(tile_setting['border_list']) == sorted(found_locs):
                        tile_row = int(tile_setting['tile'][0])
                        tile_col = int(tile_setting['tile'][-1])
                        level_map.tile_map[tuple(tile)][layer] = [selected_spritesheet, tile_row, tile_col]

def undo(level_map,undo_dat,undo_counter):
    # save current map to file
    level_map.write('data/files/json/tile_editor/undo_0.json')
    # upload current map and save it to a list
    dat = load_json('data/files/json/tile_editor/undo_0.json')['map']
    new_dat = {}
    for pos in dat:
        for layer in dat[pos]:
            new_tile_dat = {int(layer):dat[pos][layer]}
            new_dat[tuple([int(v) for v in pos.split(';')])] = new_tile_dat
    dat = new_dat
    # check for duplicates
    error = False
    for map in undo_dat:
        if dat == map:
            error = True
    # if there is no duplicates
    if error == False:
        # this removes everything in the list that is saved after current counter -- #
        undo_dat = undo_dat[:undo_counter + 1]
        # add dat from upload
        undo_dat.append(dat)
        undo_counter += 1
    # return undo_dat, undo_counter
    return undo_dat,undo_counter






# editor direction corresponds with scroll
up = False
down = False
right = False
left = False
# clicks
click = False
clicking = False
right_clicking = False
# other button presses
ctrl = False
shift = False
# change the transparency of layers
layer_opacity = False
# selection tool
current_selection = [None, None]
# scroll stuff
scroll = [0, 0]
scroll_speed = 5
# title scroll
spritesheet_scroll = 0
spritesheet_scroll_max = 0
spritesheet_scroll_img_max = 0
# tiles scroll
spritesheet_img_scroll_x = 0
spritesheet_img_scroll_y = 0
# current selection tile/spritesheet
selected_spritesheet = None
selected_tile = None
# layer
current_layer = 0
# particle effect stuff
deleted_tiles = []
particles = []
square_effects = []
# revert
undo_counter = -1
undo_dat = []

while True:
    hovering_spritesheet_list = False
    hovering_spritesheet_images = False
    display.fill((40, 40, 40))

    mx, my = pygame.mouse.get_pos()
    mx = int(mx / display_scale)
    my = int(my / display_scale)

    # arrow keys controllers scroll as well as mouse -------------- #
    if right:
        scroll[0] += scroll_speed
    if left:
        scroll[0] -= scroll_speed
    if up:
        scroll[1] -= scroll_speed
    if down:
        scroll[1] += scroll_speed

    # visible tiles list
    for layer in level_map.get_visible(scroll):
        #level_map.tile_map[]
        for tile in layer:
            offset = [0, 0]
            if tile[1][0] in offset_dat:
                tile_id = str(tile[1][1]) + ';' + str(tile[1][2])
                if tile_id in offset_dat[tile[1][0]]:
                    if 'tile_offset' in offset_dat[tile[1][0]][tile_id]:
                        offset = offset_dat[tile[1][0]][tile_id]['tile_offset']
            # tile is a the data from the specific key (tile) ------------------ #
            img = spritesheet_loader.get_img(spritesheets, tile[1])
            if layer_opacity:
                pos = (tile[0][0]//tile_size,tile[0][1]//tile_size)
                if current_layer not in level_map.tile_map[pos]:
                    img = img.copy()
                    img.set_alpha(100)
            display.blit(img,(tile[0][0] - scroll[0] + offset[0],tile[0][1] - scroll[1] + offset[1]))

    # ----------------------------------------------------------------------------------- #

    # current selection ----------------------------------------------------------------- #
    if current_selection != [None, None]:
        # if a section is selected
        selection_points = [current_selection[0], current_selection[1]]
        if current_selection[1] == None:
            # if user is selecting
            selection_points[1] = (mx + scroll[0], my + scroll[1])
        selection_r = corner_rect(selection_points)
        selection_r.x -= scroll[0]
        selection_r.y -= scroll[1]
        pygame.draw.rect(display, (255, 0, 255), selection_r, 1)
    # ------------------------------------------------------------------------------------ #

    # delete a tile  --------------------- #
    if right_clicking and (mx > side_bar_up.get_width()):
        hover_x = int(round((mx + scroll[0]) / tile_size - 0.5, 0))
        hover_y = int(round((my + scroll[1]) / tile_size - 0.5, 0))
        deleted_tile = level_map.remove_tile((hover_x, hover_y), current_layer)
        if deleted_tile:
            deleted_tiles.append(deleted_tile)
    # -------------------------------------- #

    # create side bar -------------------------------- #
    side_bar_up = pygame.Surface((100, display_size[1] // 3))
    side_bar_up.fill((20, 35, 40))
    side_bar_up_r = side_bar_up.get_rect()
    side_bar_down = pygame.Surface((100, display_size[1] - (display_size[1] // 3)))
    side_bar_down.fill((20, 35, 40))
    side_bar_down_r = side_bar_down.get_rect()
    # ------------------------------------------------ #

    # rendering sidebar buttons including spritesheet type and individual tiles ---------- #
    # render spritesheet titles and buttons -------- #
    spritesheet_scroll_max = 0
    for i, spritesheet in enumerate(spritesheets):
        spritesheet_r = pygame.Rect(0, 1 + i * 15 - spritesheet_scroll, 60, 10)
        offset_x = 0
        spritesheet_scroll_max += 15
        if spritesheet_r.collidepoint((mx, my)):
            if click:
                selected_spritesheet = spritesheet
                spritesheet_img_scroll = 0
                selected_tile = None
            offset_x = 2
        font.render(spritesheet, side_bar_up,( 2 + offset_x, 1 + i * 15 - spritesheet_scroll))
    display.blit(side_bar_up, (0, 0))
    # side bar scroll end pos
    spritesheet_scroll_max -= side_bar_up.get_height()
    # render spritesheet tiles and buttons -------- #
    if selected_spritesheet:
        y_pos = 0
        x_pos = 0
        for y, row in enumerate(spritesheets[selected_spritesheet]):
            tallest_img = 0
            spritesheet_scroll_img_max = 0
            for x, img in enumerate(row):
                offset_y = 0
                img_r = img.get_rect()
                img_r.x = 2 + x_pos - spritesheet_img_scroll
                img_r.y = 3 + y_pos + side_bar_up.get_height()
                spritesheet_scroll_img_max += img_r.y
                if img_r.collidepoint((mx, my)):
                    if click:
                        selected_tile = [selected_spritesheet, y, x]
                    offset_y = -2
                side_bar_down.blit(img, (
                    2 + x_pos - spritesheet_img_scroll_x, 3 + y_pos + offset_y - spritesheet_img_scroll_y))
                x_pos += img.get_width() + 1
                tallest_img = max(tallest_img, img.get_height())
            y_pos += tallest_img + 3
            x_pos = 0
        # side bar scroll end pos
        spritesheet_scroll_img_max -= side_bar_down.get_height()
    pygame.draw.line(side_bar_down, (32, 50, 60), (0, 0),
                     (side_bar_up.get_width(), 0))
    display.blit(side_bar_down, (0, side_bar_up.get_height()))
    # ------------------------------------------------------------------------------------- #

    # show tiles on mouse and add tile to level map ----------- #
    if selected_tile:
        img = spritesheet_loader.get_img(spritesheets, selected_tile).copy()
        img.set_alpha(150)
        hover_x = int(round((mx + scroll[0]) / tile_size - 0.5, 0))
        hover_y = int(round((my + scroll[1]) / tile_size - 0.5, 0))
        # if not in selection mode then display faded tile --- #
        if current_selection == [None, None]:
            display.blit(img, (hover_x * tile_size - scroll[0], hover_y * tile_size - scroll[1]))
        if clicking and (mx > side_bar_up.get_width()):
            # add tile
            t = level_map.add_tile( selected_tile.copy(), (hover_x, hover_y), current_layer)
    # ---------------------------------------------------------- #

    # undo update
    undo_dat,undo_counter = undo(level_map,undo_dat,undo_counter)


    # hud --------------------------------------------------------------------------------- #
    # status of said tileset and loc of tile on tile editor -------------- #
    if selected_spritesheet:
        status_str = selected_spritesheet
        if selected_tile:
            status_str += '. ' + str(selected_tile[1]) + '. ' + str(selected_tile[2])
            sel_img = spritesheet_loader.get_img(spritesheets, selected_tile)
            title_offset = font.get_size(str(status_str)) - 5
            display.blit(sel_img, (
                display.get_width() // 2 + side_bar_up.get_width() // display_size[
                    0] + sel_img.get_width() + title_offset - 20,3 ))
        # pos ------- #
        hover_x = int(round((mx + scroll[0]) / tile_size - 0.5, 0))
        hover_y = int(round((my + scroll[1]) / tile_size - 0.5, 0))
        # display hud ----------------- #
        font.render(status_str, display,(display.get_width() // 2 + side_bar_up.get_width() // display_size[0] -20, 5))
        font.render('pos x: ' + str(hover_x), display,(display.get_width() // 2 + side_bar_up.get_width() + 30, 5))
        font.render('pos y: ' + str(hover_y), display, (display.get_width() // 2 + side_bar_up.get_width() + 90, 5))
        font.render('current layer: ' + str(current_layer), display,(display.get_width() // 2 + side_bar_up.get_width() - 275, 5))

    # ------------------------------------------------------------------------------------- #

    # collisions ------------------------------------------------------ #
    # mouse in side bar, else on tile editor
    if side_bar_up_r.collidepoint((mx, my)):
        hovering_spritesheet_list = True

    if side_bar_down_r.collidepoint((mx, my)):
        hovering_spritesheet_images = True

    # buttons and mouse presses -------------------------------------- #
    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # mouse inputs ---------------------------------------------- #
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False
            if event.button == 3:
                right_clicking = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x = level_map.get_tile([20, 10])
                click = True
                clicking = True
            if event.button == 3:
                right_clicking = True
            # moves tileset titles
            if hovering_spritesheet_list:
                spritesheet_scroll_max = max(0, spritesheet_scroll_max)
                if event.button == 4:
                    spritesheet_scroll -= 9
                    spritesheet_scroll = max(0, spritesheet_scroll)
                if event.button == 5:
                    spritesheet_scroll += 9
                    spritesheet_scroll = min(spritesheet_scroll, spritesheet_scroll_max)
            # moves tiles in sidebar
            elif hovering_spritesheet_images:
                if shift:
                    if event.button == 5:
                        spritesheet_img_scroll_x -= 14
                        spritesheet_img_scroll_x = max(0, spritesheet_img_scroll_x)
                    if event.button == 4:
                        spritesheet_img_scroll_x += 14
                else:
                    spritesheet_scroll_img_max = max(0, spritesheet_scroll_img_max)
                    if event.button == 4:
                        spritesheet_img_scroll_y -= 14
                        spritesheet_img_scroll_y = max(0, spritesheet_img_scroll_y)
                    if event.button == 5:
                        spritesheet_img_scroll_y += 14
                        spritesheet_img_scroll_y = min(spritesheet_img_scroll_y, spritesheet_scroll_img_max)
            # changes layer
            else:
                if event.button == 4:
                    current_layer += 1
                if event.button == 5:
                    current_layer -= 1
        # key presses ---------------------------------------------------------------- #
        if event.type == KEYDOWN:
            # scroll control
            if (not ctrl) and (not shift):
                if event.key == K_w:
                    up = True
                if event.key == K_s:
                    down = True
                if event.key == K_d:
                    right = True
                if event.key == K_a:
                    left = True
            # shift and control presses
            if event.key == K_LSHIFT:
                shift = True
            if event.key == K_LCTRL:
                ctrl = True



            if event.key == K_SPACE:
                if ctrl:
                    if current_selection[1] != None:
                        # flood fill ------- #
                        # finds midpoint of selection
                        temp_x = int(round(abs(midpoint(current_selection)[0]) / tile_size - 0.5, 0))
                        temp_y = int(round(abs(midpoint(current_selection)[1]) / tile_size - 0.5, 0))
                        pos_list = [temp_x, temp_y]
                        # make copy of map in case of freeze --- #
                        level_map.write('data/files/json/tile_editor/fill_save_0.json')
                        # returns true or false for error
                        error = flood_fill(pos_list, level_map, selected_spritesheet, current_layer)
                        if error:
                            # if error load old map
                            level_map.load_map('data/files/json/tile_editor/fill_save_0.json')
                        # ---------------------- #
                        # auto tile ------------ #
                        # find all pos in current selection
                        auto_list = get_selection_pos_list(current_selection)
                        # auto tile will usually be your ground tileset
                        auto_tile(auto_list, level_map, current_layer, selected_spritesheet)
                        # reset current selection
                        current_selection = [None, None]
                        # ----------------------- #
            # other key actions a-z --------- #
            # auto tile
            if event.key == K_a:
                if ctrl:
                    if shift:
                        if current_selection[1] != None:
                            # find all pos in current selection
                            auto_list = get_selection_pos_list(current_selection)
                            # auto tile will usually be your ground tileset
                            auto_tile(auto_list, level_map, current_layer, selected_spritesheet)
                            # reset current selection
                            current_selection = [None, None]

            # select all
            if event.key == K_a:
                if ctrl:
                    if not shift:
                        current_selection = [(110 + scroll[0], 24 + scroll[1]), (586 + scroll[0], 383 + scroll[1])]


            # deletes all tiles in current selection
            if event.key == K_d:
                if ctrl:
                    # deleting a section of tiles
                    if current_selection[1] != None:
                        delete_list = get_selection_pos_list(current_selection)
                        for tile in delete_list:
                            deleted_tile = level_map.remove_tile(tile, current_layer)
                            if deleted_tile:
                                deleted_tiles.append(deleted_tile)
                        # reset current selection
                        current_selection = [None, None]

            # selection mode
            if event.key == K_e:
                selected_tile = None
                # if nothing is selected
                if current_selection[0] == None:
                    current_selection = [(mx + scroll[0], my + scroll[1]), None]
                # if something is selected
                elif current_selection[1] == None:
                    current_selection[1] = (mx + scroll[0], my + scroll[1])

            # flood fill
            if event.key == K_f:
                # make sure user is selecting something before filling
                hover_x = int(round((mx + scroll[0]) / tile_size - 0.5, 0))
                hover_y = int(round((my + scroll[1]) / tile_size - 0.5, 0))
                pos_list = [hover_x, hover_y]
                # make copy of map in case of freeze --- #
                level_map.write('data/files/json/tile_editor/fill_save_0.json')
                # returns true or false for error
                error = flood_fill(pos_list, level_map, selected_spritesheet, current_layer)
                if error:
                    # if error load old map
                    level_map.load_map('data/files/json/tile_editor/fill_save_0.json')

            # changes layer opacity
            if event.key == K_l:
                layer_opacity = not layer_opacity

                # save map
            if event.key == K_s:
                if ctrl:
                    level_map.write('data/files/json/prototype/save_0.json')
            if event.key == K_o:
                level_map.load_map('data/files/json/prototype/save_0.json')

            # removes current selection
            if event.key == K_r:
                current_selection = [None, None]

            if event.key == K_z:
                if ctrl:
                    # can revert fills and del but can re revert back to said fil or del ---- #
                    # make copy of undo index
                    undo_counter_c = undo_counter
                    # controls what index in the saved map list
                    if shift:
                        undo_counter += 1
                    elif not shift:
                        undo_counter -= 1
                    # stops from user causing a index error
                    if undo_counter > -1 and undo_counter < len(undo_dat):
                        level_map.tile_map = undo_dat[undo_counter].copy()
                    else:
                        undo_counter = undo_counter_c
                        level_map.tile_map = undo_dat[undo_counter].copy()

        # key releases ---------------------------------------------------------------- #
        if event.type == KEYUP:
            if (not ctrl) and (not shift):
                if event.key == K_w:
                    up = False
                if event.key == K_s:
                    down = False
                if event.key == K_d:
                    right = False
                if event.key == K_a:
                    left = False
            if event.key == K_LSHIFT:
                shift = False
            if event.key == K_LCTRL:
                ctrl = False

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)
