import numpy as np
import glm

class BaseModel:
    def __init__(self, app, vao_name, tex_id):
        self.app = app
        self.vao_name = vao_name
        self.tex_id = tex_id
        self.m_model = self.get_model_matrix()
        self.program = app.shader.programs[vao_name]
        self.camera = app.camera
        self.texture = app.texture.textures[self.tex_id]
        
    def update(self):
        self.texture.use()
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def get_model_matrix(self):
        return np.eye(4, dtype='f4')
    
    def render(self):
        self.update()
        self.app.vao.render(self.vao_name)

class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id='container', position=glm.vec3(0.0)):
        super().__init__(app, vao_name, tex_id)
        self.position = position
        self.program['texture1'] = 0
        self.program['texture2'] = 1
        self.program['m_proj'].write(self.camera.m_projection)
        self.texture2 = app.texture.textures['awesomeface']

    def update(self):
        self.texture.use(location=0)
        self.texture2.use(location=1)
        self.program['m_view'].write(self.camera.m_view)
        
        model = glm.mat4(1.0)
        model = glm.translate(model, self.position + self.app.cubeTranslation)
        model = glm.rotate(model, glm.radians(self.app.cubeRotValue.x), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(self.app.cubeRotValue.y), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(self.app.cubeRotValue.z), glm.vec3(0, 0, 1))
        model = glm.scale(model, self.app.cubeScale)
        
        self.m_model = model
        self.program['m_model'].write(self.m_model)
        
class Skybox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox'):
        super().__init__(app, vao_name, tex_id)
        self.program['u_texture_skybox'] = 0
        self.program['m_proj'].write(self.camera.m_projection)

    def update(self):
        self.texture.use(location=0)
        view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_view'].write(view)

class Heightmap(BaseModel):
    def __init__(self, app, vao_name='heightmap', tex_id='heightmap'):
        super().__init__(app, vao_name, tex_id)
        self.program['u_texture_0'] = 0
        self.program['m_proj'].write(self.camera.m_projection)
