# CMPSC 458 Project 1

Please fill out the README's content in your intermediate submission 2 and final submission.

Student Name: Abha Mam

## How to run the Project

to run the project, plus a check because my venv kept having issues installing the pygame module (mac arm64):

```bash
conda create --name graphics python=3.10 -y
conda activate graphics
pip install -e .

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python - <<'PY'
import pygame, moderngl, glm
from PIL import Image
print("all good:", pygame.__version__)

python Project1.py
PY
```
## Project description

I only edited the engine.py, which should allow you to use basic WASD commands to move the boxes around and adjust direction using your cursor.

I implemented translations (hold control and use WASD), scale (hold shift and use WASD), uniform scale (p), and a reset (r)

other controls include UJIKOL for xyz axis as mentioned in slides.

[X] heightmap
[X] skybox
[X] transformations

## Extra credit attempt

If you have attempted the extra credit, please describe what you have done here.
