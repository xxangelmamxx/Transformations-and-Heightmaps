import numpy as np
from PIL import Image
import os

class VBO:
    def __init__(self, context, heightmap_path=None):
        self.context = context
        self.vbos = {}
        self.ebos = {}
        self.formats = {}
        self.attributes = {}
        if heightmap_path is None:
            self.heightmap_path = os.path.join('Media', 'Skybox', 'field', 'bottom.jpg')
        else:
            self.heightmap_path = heightmap_path
        self.create_vbos()

    def create_vbos(self, heightmap_path=None):
        if heightmap_path is None:
            heightmap_path = self.heightmap_path
        self.create_cube_vbo()
        self.create_skybox_vbo()
        self.create_heightmap_vbo(heightmap_path)

    def create_cube_vbo(self):
        p = 0.5
        faces = [
            (-p, -p,  p), ( p, -p,  p), ( p,  p,  p), (-p,  p,  p),
            ( p, -p, -p), (-p, -p, -p), (-p,  p, -p), ( p,  p, -p),
            (-p, -p, -p), (-p, -p,  p), (-p,  p,  p), (-p,  p, -p),
            ( p, -p,  p), ( p, -p, -p), ( p,  p, -p), ( p,  p,  p),
            (-p,  p,  p), ( p,  p,  p), ( p,  p, -p), (-p,  p, -p),
            (-p, -p, -p), ( p, -p, -p), ( p, -p,  p), (-p, -p,  p),
        ]

        uvs = [
            (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        ] * 6

        verts = []
        for (px,py,pz), (u,v) in zip(faces, uvs):
            verts.extend([px, py, pz, u, v])

        inds = []
        for face in range(6):
            base = face * 4
            inds.extend([base + 0, base + 1, base + 2, base + 0, base + 2, base + 3])

        vertices = np.array(verts, dtype='f4').tobytes()
        indices = np.array(inds, dtype='u4').tobytes()

        self.vbos['cube'] = self.context.buffer(vertices)
        self.ebos['cube'] = self.context.buffer(indices)
        self.formats['cube'] = '3f 2f'
        self.attributes['cube'] = ('in_position', 'in_texcoord_0')

    def create_skybox_vbo(self):
        size = 1.0
        p = size
        faces = {
            'front':  [ (-p,-p,p), ( p,-p,p), ( p, p,p), (-p, p,p) ],
            'back':   [ ( p,-p,-p), (-p,-p,-p), (-p, p,-p), ( p, p,-p) ],
            'left':   [ (-p,-p,-p), (-p,-p,p), (-p, p,p), (-p, p,-p) ],
            'right':  [ ( p,-p,p), ( p,-p,-p), ( p, p,-p), ( p, p,p) ],
            'top':    [ (-p, p,p), ( p, p,p), ( p, p,-p), (-p, p,-p) ],
            'bottom': [ (-p,-p,-p), ( p,-p,-p), ( p,-p,p), (-p,-p,p) ],
        }

        atlas_map = {
            'top':    (1,0),
            'left':   (0,1),
            'front':  (1,1),
            'right':  (2,1),
            'back':   (3,1),
            'bottom': (1,2)
        }
        cols = 4; rows = 3

        verts = []
        inds = []
        vert_index = 0
        for face_name in ['front','back','left','right','top','bottom']:
            col, row = atlas_map[face_name]
            u0 = col / cols
            v0 = row / rows
            u1 = (col + 1) / cols
            v1 = (row + 1) / rows
            face_pos = faces[face_name]
            texcoords = [(u0,v1), (u1,v1), (u1,v0), (u0,v0)]
            for (px,py,pz), (u,v) in zip(face_pos, texcoords):
                verts.extend([px,py,pz, u, v])
            inds.extend([vert_index, vert_index+1, vert_index+2, vert_index, vert_index+2, vert_index+3])
            vert_index += 4

        vertices = np.array(verts, dtype='f4').tobytes()
        indices = np.array(inds, dtype='u4').tobytes()

        self.vbos['skybox'] = self.context.buffer(vertices)
        self.ebos['skybox'] = self.context.buffer(indices)
        self.formats['skybox'] = '3f 2f'
        self.attributes['skybox'] = ('in_position', 'in_texcoord')

    def create_heightmap_vbo(self, image_path=None):
        if image_path is None:
            image_path = self.heightmap_path

        image = Image.open(image_path).convert('L')
        width, height = image.size
        pixel_data = np.array(image, dtype=np.float32)

        max_vertices = 400000
        total_vertices = width * height
        if total_vertices > max_vertices:
            scale = (max_vertices / float(total_vertices)) ** 0.5
            new_w = max(2, int(round(width * scale)))
            new_h = max(2, int(round(height * scale)))
            image = image.resize((new_w, new_h), Image.BILINEAR)
            width, height = image.size
            pixel_data = np.array(image, dtype=np.float32)

        minv = float(pixel_data.min())
        maxv = float(pixel_data.max())
        if maxv > minv:
            pixel_norm = (pixel_data - minv) / (maxv - minv)
        else:
            pixel_norm = np.zeros_like(pixel_data, dtype=np.float32)

        invert_heights = False
        if invert_heights:
            pixel_norm = 1.0 - pixel_norm

        WORLD_SCALE_X = 1.0
        WORLD_SCALE_Z = 1.0
        height_scale = 6.0
        Y_OFFSET = -8.0

        sx = WORLD_SCALE_X
        sz = WORLD_SCALE_Z

        verts = []
        for j in range(height):
            for i in range(width):
                px = (i - (width - 1) / 2.0) * sx
                pz = (j - (height - 1) / 2.0) * sz
                py = (pixel_norm[j, i] * height_scale) + Y_OFFSET
                u = i / (width - 1) if width > 1 else 0.0
                v = j / (height - 1) if height > 1 else 0.0
                verts.extend([px, py, pz, u, v])

        inds = []
        for j in range(height - 1):
            for i in range(width - 1):
                tl = j * width + i
                tr = tl + 1
                bl = (j + 1) * width + i
                br = bl + 1
                inds.extend([tl, bl, br, tl, br, tr])

        self.vbos['heightmap'] = self.context.buffer(np.array(verts, dtype='f4').tobytes())
        self.ebos['heightmap'] = self.context.buffer(np.array(inds, dtype='u4').tobytes())
        self.formats['heightmap'] = '3f 2f'
        self.attributes['heightmap'] = ('in_position', 'in_texcoord_0')

    def destroy(self):
        for vbo in self.vbos.values():
            vbo.release()
        for ebo in self.ebos.values():
            ebo.release()
