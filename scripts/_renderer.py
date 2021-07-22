


class Renderer():
    def __init__(self,app):
        self.app = app

    def render(self):
        self.app.world.render()
