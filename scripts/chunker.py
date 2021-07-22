import math, pygame, json

# convert tuple to str
def tuple_to_str(t):
    return ';'.join([str(v) for v in t])

# convert str to tuple
def str_to_tuple(s):
    return tuple([int(v) for v in s.split(';')])

# tile map class
class TileMap():
    def __init__(self, tile_size, view_size):
        self.tile_size = tile_size
        self.view_size = view_size
        self.tile_map = {}
        self.all_layers = []

    # convert tile map to tuple
    # use after converting tile map to json
    def tuplify_map(self):
        new_tile_map = {}
        for pos in self.tile_map:
            new_tile_data = {}
            for layer in self.tile_map[pos]:
                new_tile_data[int(layer)] = self.tile_map[pos][layer]
            new_tile_map[str_to_tuple(pos)] = new_tile_data
        self.tile_map = new_tile_map

    # convert tilemap to str
    # when converting from json
    def strify_map(self):
        new_tile_map = {}
        for pos in self.tile_map:
            new_tile_map[tuple_to_str(pos)] = self.tile_map[pos]
        self.tile_map = new_tile_map

    # load map from json file
    def load_map(self, path):
        f = open(path, 'r')
        dat = f.read()
        f.close()
        json_dat = json.loads(dat)
        self.tile_map = json_dat['map']
        self.all_layers = json_dat['all_layers']
        # convert tile map to tuples
        self.tuplify_map()
        # load bounds
        #self.map_bounds()

    def map_bounds(self):
        # create list of all the x pos and y pos
        tile_x_list = [layer_dat['grid_tiles'][tile_pos]['pos'][0] for chunk in self.tile_map for layer_dat in self.tile_map[chunk]
        for tile_pos in layer_dat['grid_tiles']]
        tile_y_list = [layer_dat['grid_tiles'][tile_pos]['pos'][1] for chunk in self.tile_map for layer_dat in self.tile_map[chunk]
        for tile_pos in layer_dat['grid_tiles']]
        # find bounds for pos to find render use the product of pos and tile size
        self.left = min(tile_x_list)
        self.right = max(tile_x_list)
        self.up = min(tile_y_list)
        self.down = max(tile_y_list)

    # write map tojson file
    def write(self, path):
        # load tile map as strs
        self.strify_map()
        # save data
        json_dat = {
            'map': self.tile_map,
            'all_layers': self.all_layers
        }
        # load tile map as tuples
        self.tuplify_map()
        f = open(path, 'w')
        f.write(json.dumps(json_dat))
        f.close()

    # get pos of tile
    def get_tile(self,pos,target_layer = None):
        pos = tuple(pos)
        if pos in self.tile_map:
            if target_layer:
                if target_layer in self.tile_map[pos]:
                    return self.tile_map[pos][target_layer]
                else:
                    return None
            else:
                return self.tile_map[pos]
        else:
            return None

    # add tile to tile map
    def add_tile(self, tile_type, pos, target_layer):
        pos = tuple(pos)
        # if pos is all ready in tile map
        if pos in self.tile_map:
            self.tile_map[pos][target_layer] = tile_type
        # if pos is not in tile map set pos = {target_layer:tile_type}
        else:
            self.tile_map[pos] = {target_layer:tile_type}
        # add layer if not in all layer list
        if target_layer not in self.all_layers:
            self.all_layers.append(target_layer)
            self.all_layers.sort()


    # remove tile from tile map
    def remove_tile(self, pos, target_layer = None):
        pos = tuple(pos)
        if pos in self.tile_map:
            if target_layer:
                if target_layer in self.tile_map[pos]:
                    del self.tile_map[pos][target_layer]
            else:
                del self.tile_map[pos]

    # get visable tiles
    def get_visible(self,pos):
        # create a layers dict
        layers = {layer:[] for layer in self.all_layers}
        # itertate through all tile pos in tile map
        # for example if tile size is 12 this itertates through 12, 24, 36, ect on the x and y axis
        for y in range(math.ceil(self.view_size[1]/self.tile_size[1] + 1)):
            for x in range(math.ceil(self.view_size[0]/self.tile_size[0] + 1)):
                # finds pos relative to tile size
                tile_pos = (x + int(round(pos[0]/self.tile_size[0] - .5, 0)), y + int(round(pos[1]/self.tile_size[1] - .5, 0)))
                if tile_pos in self.tile_map:
                    for tile in self.tile_map[tile_pos]:
                        layers[tile].append(((tile_pos[0] * self.tile_size[0] , tile_pos[1] * self.tile_size[1]) ,self.tile_map[tile_pos][tile]))
        # return a list of layers with tile pos as values
        output = [layers[layer] for layer in self.all_layers]
        return output

    # get near by tiles for collisons
    def get_near_by_rects(self,pos):
        tile_pos = int(pos[0] // self.tile_size[0]), int(pos[1] // self.tile_size[1])
        check_locs = [
            [-1,0],
            [0,0],
            [1,0],
            [-1,-1],
            [0,-1],
            [1,-1],
            [-1,1],
            [0,1],
            [1,1]
                    ]
        rects = []
        for loc in check_locs:
            check_loc = (loc[0] + tile_pos[0], loc[1] + tile_pos[1])
            if check_loc in self.tile_map:
                for layer in self.tile_map[check_loc]:
                    if self.tile_map[check_loc][layer][0] == 'ground':
                        rects.append(pygame.Rect(check_loc[0] * self.tile_size[0],check_loc[1] * self.tile_size[1],self.tile_size[0],self.tile_size[1]))
        # return rects
        return rects
