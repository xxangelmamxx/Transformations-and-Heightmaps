class Shader:
    def __init__(self, context):
        self.context = context
        self.programs = {}
        self.programs['default'] = self.get_program(shader_name='default')
        self.programs['skybox'] = self.get_program(shader_name='skybox')
        self.programs['heightmap'] = self.get_program(shader_name='default')
        self.programs['cube'] = self.get_program(shader_name='container')
    
    
    def get_program(self, shader_name='default', shader_path='Media/Shaders'):
        """ Load the appropriate vertex and fragment shaders and create a program.

        Args:
            shader_name (str, optional): _description_. Defaults to 'default'.
            shader_path (str, optional): _description_. Defaults to 'Media/Shaders'.

        Returns:
            _type_: _description_
        """
        with open(f'{shader_path}/{shader_name}.vert', 'r') as file:
            vertex_shader = file.read()
            
        with open(f'{shader_path}/{shader_name}.frag', 'r') as file:
            fragment_shader = file.read()
       
        program = self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        for program in self.programs.values():
            program.release()
        self.programs.clear()