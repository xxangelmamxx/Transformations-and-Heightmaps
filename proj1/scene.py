from proj1.model import *
import glm

class Scene:
    def __init__(self, app):
        self.app = app
        self.cubes = []
        self.skybox = None
        self.heightmap = None
        self.load()
    
    def load(self):
        app = self.app
        cube_positions = [
            glm.vec3(0.0, 0.0, 0.0),
            glm.vec3(2.0, 5.0, -15.0),
            glm.vec3(-1.5, -2.2, -2.5),
            glm.vec3(-3.8, -2.0, -12.3),
            glm.vec3(2.4, -0.4, -3.5),
            glm.vec3(-1.7, 3.0, -7.5),
            glm.vec3(1.3, -2.0, -2.5),
            glm.vec3(1.5, 2.0, -2.5),
            glm.vec3(-2.0, 0.5, -3.5),
            glm.vec3(0.0, 3.0, -10.0),
        ]
        self.cubes = [Cube(app, position=pos) for pos in cube_positions]
        self.skybox = Skybox(app)
        self.heightmap = Heightmap(app)
       
    def update(self):
        for cube in self.cubes:
            cube.update()
        if self.skybox:
            self.skybox.update()
        if self.heightmap is not None:
            self.heightmap.update()
             
    def render(self):
        for obj in self.cubes:
            obj.render()
        if self.skybox:
            self.skybox.render()
        if self.heightmap is not None:
            self.heightmap.render()
