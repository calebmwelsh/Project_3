from .entity import Entity
from .entity_objs.player import Player


class EntityManager:
    def __init__(self,game):
        self.game = game
        self.entities = []
        self.entities.append(Player(game, self.game.assets.animations, [230,0], (10, 16), 'player'))
        self.player = self.entities[0]

    # update entities
    def update(self):
        for entity in self.entities:
            entity.update(self.game.window.dt)

    # render entities
    def render(self):
        for entity in self.entities:
            entity.render(self.game.window.display,self.game.world.camera.pos)
