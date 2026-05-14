class VAO:
    def __init__(self, app):
        self.context = app.context
        self.vbo = app.vbo
        self.shader = app.shader 
        self.vaos = {}
        self.create_vaos()

    def create_vaos(self):
        for name, vbo_buffer in self.vbo.vbos.items():
            program = self.shader.programs.get(name, self.shader.programs.get('default'))
            fmt = self.vbo.formats.get(name)
            attrs = self.vbo.attributes.get(name)
            if fmt and attrs:
                try:
                    vao = self.context.vertex_array(program, [(vbo_buffer, fmt, *attrs)], index_buffer=self.vbo.ebos.get(name))
                    self.vaos[name] = vao
                except Exception as e:
                    print(f"VAO creation failed for {name}: {e}")
                    continue

    def render(self, vao_name):
        vao = self.vaos.get(vao_name)
        if vao:
            vao.render()
    
    def destroy(self):
        [vao.release() for vao in self.vaos.values()]
