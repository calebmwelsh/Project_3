


class Renderer():
    def __init__(self,game):
        self.game = game

    def render(self):
        self.game.world.render()
