import math

class Camera:
    def __init__(self, game):
        self.game = game
        self.true_pos = [0,0]
        self.target_pos = [0,0]
        self.rate = [.8,.2]
        self.tracked_entity = None

    # set target pos
    def set_target(self,pos):
        self.target_pos = list(pos)

    # set target entity
    def set_tracked_entity(self,entity):
        self.tracked_entity = entity

    # update camera
    def update(self):
        if self.tracked_entity:
            temp_x = self.tracked_entity.pos[0] - self.game.window.display.get_width() // 2
            temp_y = self.tracked_entity.pos[1] - self.game.window.display.get_height() // 2
            self.set_target((temp_x,temp_y))
        self.true_pos[0] += (self.target_pos[0] - self.true_pos[0]) / (self.rate[0] / self.game.window.dt)
        self.true_pos[1] += (self.target_pos[1] - self.true_pos[1]) / (self.rate[1] / self.game.window.dt)

    # floored pos
    @ property
    def pos(self):
        return ( int(math.floor(self.true_pos[0])) , int(math.floor(self.true_pos[1])) )
