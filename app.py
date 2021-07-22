# import attributes
from scripts._window import Window
from scripts._input import Input
from scripts._renderer import Renderer
from scripts._world import World
from scripts._assets import Assets

# app object
class App:
    # initation
    def __init__(self):
        # app attributes
        self.window = Window(self)
        self.input = Input(self)
        self.renderer = Renderer(self)
        self.assets = Assets(self)
        self.world = World(self)

    # update app
    def update(self):
        self.input.update()
        self.world.update()
        self.renderer.render()
        self.window.render_frame()

    # run app
    def run(self):
        while True:
            self.update()

# app
App().run()
