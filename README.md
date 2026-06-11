# A Study of 3D Transformations and Heightmap-Based Terrain Rendering

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pygame-00A300?logo=python&logoColor=white" alt="Pygame">
  <img src="https://img.shields.io/badge/ModernGL-5586A4?logo=opengl&logoColor=white" alt="ModernGL">
  <img src="https://img.shields.io/badge/OpenGL-5586A4?logo=opengl&logoColor=white" alt="OpenGL">
  <img src="https://img.shields.io/badge/PyGLM-4B8BBE?logo=python&logoColor=white" alt="PyGLM">
  <img src="https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Pillow-8A2BE2?logo=python&logoColor=white" alt="Pillow">
</p>

This project is an interactive 3D graphics study built with Python, Pygame, ModernGL, PyGLM, NumPy, and Pillow. It explores how a real-time scene is assembled from vertex data, shader programs, textures, transformation matrices, camera movement, and image-based terrain generation.

Rather than treating the scene as a finished game or isolated assignment, this repository studies the graphics pipeline step by step. The program shows how multiple textured cubes can be transformed in 3D space, how a camera can move through the world, how a skybox can create the illusion of a surrounding environment, and how a grayscale image can be interpreted as terrain height data.

The main entry point is:

```bash
python Project1.py
```

When the program runs, it opens an OpenGL window and renders a small 3D world containing textured cubes, a surrounding skybox, and a heightmap-generated surface.

---


## Abstract

This project investigates the relationship between object-space geometry, world-space transformations, camera-space viewing, projection, texture mapping, and terrain generation. The application renders a scene using ModernGL and demonstrates how the GPU receives structured vertex data through vertex buffer objects, how shaders convert that data into pixels, and how matrix operations control the final placement of objects on the screen.

The central idea is that a 3D scene is not stored as a picture. It is built from mathematical data. Cubes are defined by vertices and texture coordinates. The terrain is produced from image brightness values. The camera is represented by view and projection matrices. The final image appears only after the vertex shader, fragment shader, textures, and transformation matrices work together during rendering.

The project focuses on three connected topics:

1. **Transformations**: translating, rotating, and scaling cube geometry through model matrices.
2. **Heightmaps**: converting grayscale image values into a 3D terrain mesh.
3. **Scene context**: using a movable camera and skybox to make the 3D environment feel spatially complete.

---

## Focus

The project is organized around the following graphics questions:

- How does raw vertex data become a visible 3D object?
- How do model, view, and projection matrices work together?
- How can keyboard input change object transformations in real time?
- How can a 2D grayscale image become a 3D surface?
- How does a skybox create the illusion of a surrounding world?
- How are textures connected to geometry through UV coordinates?
- How does the CPU-side Python code communicate rendering instructions to the GPU?

Each major part of the code answers one part of these questions.

---

## Technologies Used

The project uses the following libraries:

| Technology | Role in the Project |
|---|---|
| Python | Main programming language |
| Pygame | Window creation, event handling, keyboard input, and mouse input |
| ModernGL | OpenGL rendering interface |
| PyGLM | Vector and matrix math for camera and transformations |
| NumPy | Efficient numeric arrays for vertex and index data |
| Pillow | Image loading and grayscale conversion for the heightmap |

The dependency list is stored in `requirements.txt`:

```txt
pygame
moderngl
numpy
PyGLM
Pillow
```

---

## Running the Study

Run the project from the repository root. This matters because the code loads shaders, textures, skybox images, and heightmap sources using relative paths such as `Media/Shaders`, `Media/textures`, and `Media/Skybox/field`.

### Conda Setup

```bash
conda create --name graphics python=3.10 -y
conda activate graphics
pip install -r requirements.txt
pip install -e .
python Project1.py
```

### Python Virtual Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
python Project1.py
```

On Windows, activate the virtual environment with:

```bash
.venv\Scripts\activate
```

### Quick Dependency Check

```bash
python - <<'PY'
import pygame
import moderngl
import glm
import numpy
from PIL import Image

print("All required packages imported successfully.")
print("pygame:", pygame.__version__)
PY
```

---

## Scene Overview

The rendered world contains three main visual systems:

1. **A collection of textured cubes**  
   The cubes are placed at different world positions. They share the same transformation state, so rotation, translation, and scaling controls affect the group together.

2. **A heightmap terrain surface**  
   The terrain is generated from a grayscale image. Each image pixel becomes a vertex, and the brightness of the pixel determines the vertical height of that vertex.

3. **A skybox environment**  
   Six images are arranged into a texture atlas and mapped onto a large cube surrounding the scene. This gives the world a background and makes the camera movement feel more spatial.

The camera can move independently through the scene, allowing the user to observe how the cubes, terrain, and skybox relate to one another in 3D space.

---

## Controls

The controls are divided into camera movement and object transformation.

### Camera Controls

| Input | Effect |
|---|---|
| `W` | Move forward |
| `S` | Move backward |
| `A` | Move left |
| `D` | Move right |
| `Space` | Move upward |
| `C` | Move downward |
| Mouse movement | Look around by changing camera yaw and pitch |
| `Esc` | Exit the program |

The camera behaves like a simple first-person camera. The mouse controls where the camera is looking, while the keyboard moves the camera along its forward, right, and up vectors.

### Transformation Controls

The transformation controls are loaded from `Media/controls.csv`. The same keys are reused for rotation, translation, and scaling depending on which modifier key is held.

| Key | Axis | No Modifier | Hold `Ctrl` | Hold `Shift` |
|---|---:|---|---|---|
| `U` | X | Rotate +X | Translate +X | Scale +X |
| `J` | X | Rotate -X | Translate -X | Scale -X |
| `I` | Y | Rotate +Y | Translate +Y | Scale +Y |
| `K` | Y | Rotate -Y | Translate -Y | Scale -Y |
| `O` | Z | Rotate +Z | Translate +Z | Scale +Z |
| `L` | Z | Rotate -Z | Translate -Z | Scale -Z |

Additional controls:

| Input | Effect |
|---|---|
| `P` | Uniformly increase scale on all axes |
| `R` | Reset rotation, translation, and scale |

A small implementation detail is worth noting: the CSV file uses a column named `alt`, but the engine checks for the `Shift` modifier when reading that column. In practice, `Shift` activates the scale actions.

---

## Study of the Transformation System

The transformation system is mainly implemented in `proj1/engine.py` and `proj1/model.py`.

The engine stores the active transformation state in four variables:

```python
self.cubeRotRate = glm.vec3(0.0)
self.cubeRotValue = glm.vec3(0.0)
self.cubeScale = glm.vec3(1.0)
self.cubeTranslation = glm.vec3(0.0)
```

These variables are stored once at the engine level. This means the cubes do not each have separate transformation controls. Instead, every cube reads the same rotation, translation, and scale values from the engine.

This design makes the cubes behave as a shared transformation study. The point is not to manipulate one object at a time, but to observe how changing the same transformation values affects a group of objects already placed at different positions in the scene.

### Rotation

Rotation is represented with two vectors:

- `cubeRotRate`: how quickly the rotation is changing.
- `cubeRotValue`: the accumulated rotation currently applied to the cubes.

When a rotation key is held, the engine changes the rotation rate for the selected axis. During every update cycle, the current rotation value is advanced using elapsed time:

```python
self.cubeRotValue += self.cubeRotRate * self.dt
```

This creates continuous rotation behavior. The rotation is not just a one-time jump. Instead, the cubes keep rotating based on the accumulated rotation rate. The code then wraps each rotation value within a 0 to 360 degree range:

```python
self.cubeRotValue.x %= 360.0
self.cubeRotValue.y %= 360.0
self.cubeRotValue.z %= 360.0
```

This keeps the rotation values readable and prevents them from growing endlessly.

### Translation

Translation is stored in `cubeTranslation`. When `Ctrl` is held with one of the transformation keys, the translation vector changes along the selected axis.

For example, `Ctrl + U` changes the X translation in the positive direction, while `Ctrl + J` changes the X translation in the negative direction. The same pattern applies to the Y and Z axes.

The translation value is added to each cube's original position when the model matrix is built:

```python
model = glm.translate(model, self.position + self.app.cubeTranslation)
```

This means each cube keeps its own base position, but all cubes receive the same additional translation offset.

### Scaling

Scaling is stored in `cubeScale`. Holding `Shift` with a transformation key changes the scale on a specific axis. This allows non-uniform scaling, where an object can be stretched or compressed differently along X, Y, or Z.

The `P` key increases all three scale values at the same time:

```python
self.cubeScale += glm.vec3(SCALE_STEP * self.dt)
```

This creates uniform scaling because X, Y, and Z are changed equally.

### Reset Behavior

Pressing `R` restores the transformation state:

```python
self.cubeRotRate = glm.vec3(0.0)
self.cubeRotValue = glm.vec3(0.0)
self.cubeTranslation = glm.vec3(0.0)
self.cubeScale = glm.vec3(1.0)
```

This returns the cubes to their original orientation, original offset, and normal size.

---

## Model, View, and Projection Matrix Study

A major part of the project is the relationship between three matrices:

1. **Model matrix**  
   Places an object into the world.

2. **View matrix**  
   Represents the camera's position and direction.

3. **Projection matrix**  
   Converts the 3D camera view into a perspective image on the 2D screen.

For each cube, the model matrix is rebuilt in `Cube.update()`:

```python
model = glm.mat4(1.0)
model = glm.translate(model, self.position + self.app.cubeTranslation)
model = glm.rotate(model, glm.radians(self.app.cubeRotValue.x), glm.vec3(1, 0, 0))
model = glm.rotate(model, glm.radians(self.app.cubeRotValue.y), glm.vec3(0, 1, 0))
model = glm.rotate(model, glm.radians(self.app.cubeRotValue.z), glm.vec3(0, 0, 1))
model = glm.scale(model, self.app.cubeScale)
```

This matrix begins as the identity matrix. It is then modified by translation, rotation, and scaling operations. The final matrix is sent to the shader as `m_model`.

The vertex shader combines the three matrices:

```glsl
gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
```

This line is one of the most important parts of the graphics pipeline. It shows that vertex positions are transformed in stages. A vertex begins in object space, moves into world space through the model matrix, moves into camera space through the view matrix, and is finally projected onto the screen through the projection matrix.

---

## Study of the Heightmap Terrain

The heightmap system is implemented in `proj1/vbo.py` and rendered through the `Heightmap` class in `proj1/model.py`.

A heightmap is a 2D image that stores height information. The image does not directly contain 3D geometry. Instead, the program interprets the brightness of each pixel as a height value.

The image is loaded and converted to grayscale:

```python
image = Image.open(image_path).convert('L')
```

The grayscale image is then converted into a NumPy array:

```python
pixel_data = np.array(image, dtype=np.float32)
```

Each element in the array represents the brightness of one pixel. Brighter pixels become higher terrain points, and darker pixels become lower terrain points.

### Default Heightmap Source

By default, the heightmap is generated from:

```txt
Media/Skybox/field/bottom.jpg
```

The repository also contains additional heightmap images:

```txt
Media/heightmaps/hflab4.jpg
Media/heightmaps/spiral.jpg
```

These can be used by changing the heightmap path passed into the `VBO` system or by modifying the default path in `proj1/vbo.py`.

### Normalizing Pixel Values

Before creating the terrain, the pixel brightness values are normalized:

```python
minv = float(pixel_data.min())
maxv = float(pixel_data.max())
pixel_norm = (pixel_data - minv) / (maxv - minv)
```

This maps the darkest value in the image to `0.0` and the brightest value in the image to `1.0`. Normalization makes the terrain generation more flexible because the source image does not need to use the full black-to-white range perfectly.

The code also handles the case where every pixel has the same brightness. If the image has no brightness variation, the normalized height data becomes a flat array of zeros instead of causing a division-by-zero error.

### Converting Pixels into Vertices

Each pixel becomes a vertex with five values:

```txt
x, y, z, u, v
```

The first three values are the 3D position. The final two values are texture coordinates.

The X and Z values come from the pixel's location in the image grid. The Y value comes from the normalized pixel brightness:

```python
py = (pixel_norm[j, i] * height_scale) + Y_OFFSET
```

The current constants are:

```python
height_scale = 6.0
Y_OFFSET = -8.0
```

`height_scale` controls how tall the terrain features become. `Y_OFFSET` moves the entire terrain downward in the world so it sits below the cubes and camera.

### Creating Triangle Indices

The heightmap is rendered as a mesh of triangles. Each rectangular cell in the image grid is divided into two triangles:

```python
inds.extend([tl, bl, br, tl, br, tr])
```

This allows the GPU to render the heightmap as a continuous surface rather than as disconnected points.

### Size Protection

The heightmap generator includes a vertex limit:

```python
max_vertices = 400000
```

If the image is too large, it is resized before the mesh is generated. This protects the program from creating too much vertex data and slowing down the rendering process.

---

## Study of Texture Mapping

Textures are loaded in `proj1/texture.py` and connected to geometry through UV coordinates stored in the VBOs.

The cube geometry stores a position and texture coordinate for each vertex. The format used by the cube VBO is:

```python
self.formats['cube'] = '3f 2f'
```

This means each vertex contains:

- 3 floating-point values for position.
- 2 floating-point values for texture coordinates.

The cube shader uses two texture samplers:

```python
self.program['texture1'] = 0
self.program['texture2'] = 1
```

The cube binds the container texture to texture unit 0 and the awesome-face texture to texture unit 1:

```python
self.texture.use(location=0)
self.texture2.use(location=1)
```

The fragment shader blends the two textures:

```glsl
FragColor = mix(texture(texture1, TexCoord), texture(texture2, TexCoord), 0.2);
```

This means the final cube color is mostly the container texture, with a smaller amount of the second texture blended in.

---

## Study of the Skybox

The skybox gives the scene an environmental background. It is implemented across `proj1/texture.py`, `proj1/vbo.py`, `proj1/model.py`, and the skybox shader files.

The skybox images are stored in:

```txt
Media/Skybox/field/
```

The folder contains six images:

```txt
front.jpg
back.jpg
left.jpg
right.jpg
top.jpg
bottom.jpg
```

### Texture Atlas Design

Instead of using an OpenGL cube map, this project creates a 2D texture atlas. A texture atlas combines multiple images into one larger image. The six skybox faces are arranged into a 4-column by 3-row layout:

```txt
        [ top ]
[left] [front] [right] [back]
        [bottom]
```

The atlas is created in `Texture.get_texture_skybox()`. The skybox VBO then assigns UV coordinates so each face of the skybox samples the correct part of the atlas.

### Why Camera Translation Is Removed

A skybox should feel infinitely far away. If it moved exactly like a normal object, the camera would eventually appear to approach or pass through it. To avoid this, the skybox uses the camera's rotation but removes the camera's translation:

```python
view = glm.mat4(glm.mat3(self.camera.m_view))
```

This keeps the skybox visually centered around the camera. The skybox rotates as the camera looks around, but it does not shift position when the camera moves.

The skybox vertex shader also forces the skybox to stay behind the rest of the scene:

```glsl
gl_Position = pos.xyww;
```

---

## Rendering Pipeline

The rendering process follows a standard real-time graphics structure.

### 1. Engine Initialization

`Engine.__init__()` initializes the main systems:

- Pygame window
- OpenGL context
- ModernGL context
- Depth testing
- Camera
- Shader manager
- Texture manager
- Vertex buffer objects
- Vertex array objects
- Scene objects

### 2. Input Processing

Every frame, the engine checks for keyboard and mouse input. Camera input changes the camera position and direction. Transformation input changes the cube rotation, translation, and scale values.

### 3. Scene Update

The engine updates time, camera matrices, transformation values, and scene objects. The cube model matrices are rebuilt from the current transformation state.

### 4. Rendering

The screen is cleared, scene objects are rendered, and the display buffer is swapped:

```python
self.context.clear(0.1, 0.1, 0.1)
self.scene.render()
pg.display.flip()
```

The simplified flow is:

```txt
Project1.py
   -> Engine
      -> Camera
      -> Shader
      -> Texture
      -> VBO
      -> VAO
      -> Scene
         -> Cubes
         -> Skybox
         -> Heightmap
```

---

## Project Structure

```txt
Transformations-and-Heightmaps-main/
├── Project1.py
├── README.md
├── requirements.txt
├── setup.py
├── setup.md
├── Media/
│   ├── controls.csv
│   ├── Shaders/
│   ├── Skybox/
│   ├── heightmaps/
│   └── textures/
└── proj1/
    ├── __init__.py
    ├── camera.py
    ├── engine.py
    ├── model.py
    ├── scene.py
    ├── shader.py
    ├── texture.py
    ├── util.py
    ├── vao.py
    └── vbo.py
```

---

## File-by-File Analysis

### `Project1.py`

This is the entry point. It creates the engine with an `800 x 600` window and starts the main loop.

### `proj1/engine.py`

This is the central controller of the application. It initializes the window, OpenGL context, camera, shaders, textures, VBOs, VAOs, and scene. It also handles input, updates transformation values, renders the scene, and releases resources.

The main transformation constants are:

```python
FPS = 60
ROTATION_STEP = 30
TRANSLATION_STEP = 0.5
SCALE_STEP = 1
```

### `proj1/camera.py`

This file defines the first-person camera. It stores the camera position, yaw, pitch, forward vector, right vector, up vector, view matrix, and projection matrix.

The camera turns mouse movement into changes in yaw and pitch. It turns keyboard input into movement through 3D space.

### `proj1/scene.py`

This file creates and manages the objects in the world. It adds the cube objects, the skybox, and the heightmap to the scene.

### `proj1/model.py`

This file defines renderable model classes:

- `BaseModel`
- `Cube`
- `Skybox`
- `Heightmap`

Each class is responsible for preparing its shader uniforms and rendering its assigned VAO.

### `proj1/vbo.py`

This file creates the vertex and index buffer data for the cube, skybox, and heightmap. It is especially important for the heightmap because it converts image pixels into a triangle mesh.

### `proj1/vao.py`

This file connects shader programs, vertex buffers, index buffers, and vertex attribute layouts. The VAO makes it possible to render named geometry such as `cube`, `skybox`, and `heightmap`.

### `proj1/shader.py`

This file loads and compiles GLSL shader programs from the `Media/Shaders` directory.

The project uses:

- `default.vert` and `default.frag`
- `container.vert` and `container.frag`
- `skybox.vert` and `skybox.frag`

### `proj1/texture.py`

This file loads image files and creates ModernGL textures. It also builds the skybox texture atlas from six individual skybox images.

### `proj1/util.py`

This file contains `load_controls()`, which reads `Media/controls.csv` and turns it into a dictionary used by the engine's input system.

---

## Observations

Several graphics concepts become clear through this implementation.

First, transformations are easiest to manage when they are separated into translation, rotation, and scale values before being combined into a model matrix. This makes the code easier to reason about and allows each transformation type to be controlled independently.

Second, a heightmap is a practical example of turning image data into geometry. The image is not simply drawn on the screen. It becomes a source of numerical height values, and those values are converted into vertices and triangles.

Third, the skybox demonstrates that not all objects in a scene should behave the same way. Normal objects need full model and view transformations, but the skybox needs camera rotation without camera translation so it remains visually distant.

Fourth, the rendering pipeline depends on cooperation between CPU-side code and GPU-side shaders. Python prepares the buffers, textures, matrices, and uniforms. The shader programs then use that information to transform vertices and color fragments.

---

## Limitations and Future Improvements

This study intentionally keeps the scene simple, but there are several ways it could be extended.

One limitation is that all cubes share the same transformation state. A future version could allow selecting individual cubes and transforming them independently.

Another limitation is that scaling is not clamped. If negative scaling continues long enough, an object can shrink too far or invert. A future version could enforce a minimum scale value.

The heightmap also uses a simple height calculation and does not compute lighting normals for the terrain. Adding normal generation would make the terrain respond to light more realistically.

The skybox uses a 2D atlas instead of a true cube map. A cube map implementation would be more traditional for skybox rendering and could reduce texture-coordinate complexity.

Possible future improvements include:

- Individual object selection.
- Per-object transformation controls.
- Terrain normals and lighting.
- True cube map skybox sampling.
- Heightmap source switching at runtime.
- On-screen control display.
- Camera speed adjustment.
- Clamped scaling to prevent inversion.

---

## Troubleshooting

### Import Errors

If Python cannot find one of the required packages, reinstall the dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

### Missing Media Files

If shaders, textures, or skybox images cannot be found, make sure the project is being run from the repository root:

```bash
python Project1.py
```

Running the file from inside the `proj1` folder can break the relative paths.

### Mouse Locked in the Window

The engine intentionally hides and grabs the mouse for first-person camera movement:

```python
pg.mouse.set_visible(False)
pg.event.set_grab(True)
```

Press `Esc` to exit the program and release the mouse.

### ModernGL or Pygame Installation Issues

Using a Conda environment with Python 3.10 can help avoid installation problems:

```bash
conda create --name graphics python=3.10 -y
conda activate graphics
pip install -r requirements.txt
pip install -e .
```

---

## Conclusion

This project demonstrates how a real-time 3D scene can be built from mathematical representations rather than static images. Cubes are constructed from vertex data, transformed through model matrices, viewed through a camera matrix, projected onto the screen, and textured through fragment shaders. The heightmap extends this idea by showing how an ordinary grayscale image can become a 3D terrain mesh. The skybox completes the scene by creating a surrounding environment that responds to camera rotation while remaining visually distant.

Together, these systems form a compact study of the modern graphics pipeline: data begins as vertices, images, and matrices, then becomes an interactive 3D world through OpenGL rendering.
