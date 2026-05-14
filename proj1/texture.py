import pygame as pg
from PIL import Image
import os

class Texture:
    def __init__(self, context):
        self.context = context
        self.textures = {}
        self.textures['container'] = self.get_texture('Media/textures/container.jpg')
        self.textures['awesomeface'] = self.get_texture('Media/textures/awesomeface.png', alpha=True, flip=False)
        self.textures['skybox'] = self.get_texture_skybox('Media/Skybox/field', 'jpg')
        self.textures['heightmap'] = self.get_texture('Media/textures/hdstone.jpg')
    
    def get_texture_skybox(self, texutre_dir='Media/Skybox/field', texture_ext='jpg'):
        face_files = {
            'front': 'front.' + texture_ext,
            'back':  'back.' + texture_ext,
            'left':  'right.' + texture_ext,
            'right': 'left.' + texture_ext,
            'top':   'top.' + texture_ext,
            'bottom':'bottom.' + texture_ext
        }

        imgs_by_name = {}
        base_path = texutre_dir
        order = ['front', 'back', 'left', 'right', 'top', 'bottom']
        for name in order:
            p = os.path.join(base_path, face_files[name])
            img = Image.open(p).convert('RGB')
            if name == 'top':
                img = img.rotate(270)
            if name == 'bottom':
                img = img.rotate(-90, expand=True)
                img = img.rotate(-90, expand=True)
                img = img.rotate(-90, expand=True)
            imgs_by_name[name] = img

        left_img = imgs_by_name.get('left')
        if left_img is not None:
            cell_w, cell_h = left_img.size
        else:
            front_img = imgs_by_name.get('front')
            cell_w, cell_h = front_img.size if front_img is not None else (256, 256)

        top_img = imgs_by_name['top'].resize((cell_w, cell_h), Image.BILINEAR)
        bottom_img = imgs_by_name['bottom'].resize((cell_w, cell_h), Image.BILINEAR)
        imgs_by_name['top'] = top_img
        imgs_by_name['bottom'] = bottom_img

        atlas_w = cell_w * 4
        atlas_h = cell_h * 3
        atlas = Image.new('RGB', (atlas_w, atlas_h))

        positions = {
            'top':    (1 * cell_w, 0 * cell_h),
            'left':   (0 * cell_w, 1 * cell_h),
            'front':  (1 * cell_w, 1 * cell_h),
            'right':  (2 * cell_w, 1 * cell_h),
            'back':   (3 * cell_w, 1 * cell_h),
            'bottom': (1 * cell_w, 2 * cell_h)
        }

        for name in order:
            img = imgs_by_name[name]
            pos_x, pos_y = positions[name]
            img_w, img_h = img.size
            paste_x = pos_x + max(0, (cell_w - img_w) // 2)
            paste_y = pos_y + max(0, (cell_h - img_h) // 2)
            atlas.paste(img, (paste_x, paste_y))

        atlas_data = atlas.tobytes()
        texture = self.context.texture((atlas.width, atlas.height), 3, atlas_data)
        return texture

    def get_texture(self, path, alpha=False, flip=True):
        texture = pg.image.load(path)
        if flip:
            texture = pg.transform.flip(texture, False, True)
        if alpha:
            texture = texture.convert_alpha()
            components = 4
            format = 'RGBA'
        else:
            texture = texture.convert()
            components = 3
            format = 'RGB'
        
        texture_data = pg.image.tostring(texture, format)
        texture = self.context.texture(
            size=texture.get_size(),
            components=components,
            data=texture_data
        )
        return texture

    def destroy(self):
        for texture in self.textures.values():
            texture.release()
