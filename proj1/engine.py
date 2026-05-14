import pygame as pg
import moderngl as mgl
import glm
import sys

from proj1.camera import Camera
from proj1.scene import Scene
from proj1.shader import Shader
from proj1.texture import Texture
from proj1.vao import VAO
from proj1.vbo import VBO
from proj1.util import load_controls

# Please feel free to change/add/remove any of the following constants
FPS = 60 # frames per second
ROTATION_STEP = 30# degrees per second
TRANSLATION_STEP = 0.5 # units per second
SCALE_STEP = 1 # scale units per second

class Engine:
    """
    Main engine class for the 3D application.
    Handles initialization, input processing, updates, and rendering.
    """

    def __init__(self, width=800, height=600):
        """
        Initialize the Engine with given window dimensions.

        Args:
            width (int): Window width in pixels.
            height (int): Window height in pixels.
        """
        pg.init()
        self.window_size = (width, height)
        # Set OpenGL context attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        self.screen = pg.display.set_mode(self.window_size, pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption("Project 1")
        self.context = mgl.create_context()
        self.context.enable(mgl.DEPTH_TEST)
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

        # Initialize components
        self.camera = Camera(self)
        self.shader = Shader(self.context)
        self.texture = Texture(self.context)
        self.vbo = VBO(self.context)
        self.vao = VAO(self)
        self.scene = Scene(self)

        # Cube transformation variables
        self.cubeRotRate = glm.vec3(0.0)
        self.cubeRotValue = glm.vec3(0.0)
        self.cubeScale = glm.vec3(1.0)
        self.cubeTranslation = glm.vec3(0.0)
        
        # Load control settings
        self.controls = load_controls()

    def check_events(self):
        """Check for pygame events, including quit events."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.destroy()
                pg.quit()
                sys.exit()

    def process_input(self):
        """Handle discrete camera movement input."""
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.camera.process_keyboard('FORWARD', self.dt)
        if keys[pg.K_s]:
            self.camera.process_keyboard('BACKWARD', self.dt)
        if keys[pg.K_a]:
            self.camera.process_keyboard('LEFT', self.dt)
        if keys[pg.K_d]:
            self.camera.process_keyboard('RIGHT', self.dt)
        if keys[pg.K_SPACE]:
            self.camera.process_keyboard('UP', self.dt)
        if keys[pg.K_c]:
            self.camera.process_keyboard('DOWN', self.dt)

    def apply_transformation(self, action, axis):
        i = 'xyz'.index(axis)  # x=0, y=1, z=2

        if action == 'rotate_pos':
            self.cubeRotRate[i] += ROTATION_STEP * self.dt
        elif action == 'rotate_neg':
            self.cubeRotRate[i] -= ROTATION_STEP * self.dt

        elif action == 'translate_pos':
            self.cubeTranslation[i] += TRANSLATION_STEP * self.dt
        elif action == 'translate_neg':
            self.cubeTranslation[i] -= TRANSLATION_STEP * self.dt

        elif action == 'scale_pos':
            self.cubeScale[i] += SCALE_STEP * self.dt
        elif action == 'scale_neg':
            self.cubeScale[i] -= SCALE_STEP * self.dt

    def handle_continuous_input(self):
        """Handle continuous transformation inputs based on controls."""
        keys = pg.key.get_pressed()
        mods = pg.key.get_mods()

        for key_name, actions in self.controls.items():
            key = getattr(pg, f'K_{key_name.lower()}')
            if keys[key]:
                if mods & pg.KMOD_CTRL:
                    action = actions['ctrl']
                elif mods & pg.KMOD_SHIFT:
                    action = actions['alt']
                else:
                    action = actions['no_modifier']

                axis = actions['axis']
                self.apply_transformation(action, axis)

        if keys[pg.K_r]:
            self.reset_transformations()
        if keys[pg.K_p]:
            self.cubeScale += glm.vec3(SCALE_STEP * self.dt)

    def reset_transformations(self):
        """Reset cube transformations."""
        self.cubeRotRate = glm.vec3(0.0)
        self.cubeRotValue = glm.vec3(0.0)
        self.cubeTranslation = glm.vec3(0.0)
        self.cubeScale = glm.vec3(1.0)

    def update(self):
        """Update game state, including time, input, and scene elements."""
        self.dt = self.clock.tick(FPS) / 1000.0
        self.time = pg.time.get_ticks() * 0.001
        self.process_input()
        self.handle_continuous_input()
        
        # Update rotation values based on rotation rates
        self.cubeRotValue += self.cubeRotRate * self.dt

        # Wrap rotation values to stay within 0-360 degrees
        self.cubeRotValue.x %= 360.0
        self.cubeRotValue.y %= 360.0
        self.cubeRotValue.z %= 360.0

        self.camera.update()
        self.scene.update()

    def render(self):
        """Render the scene."""
        self.context.clear(0.1, 0.1, 0.1)  
        self.scene.render()
        pg.display.flip()
       
    def run(self):
        """Main game loop."""
        while True:
            self.check_events()
            self.update()
            self.render()

    def destroy(self):
        """Clean up resources."""
        self.vbo.destroy()
        self.shader.destroy()
        self.vao.destroy()
        self.texture.destroy()
