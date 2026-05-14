We encourage students to use virtual environment for this and all projects. Specifically, we recommend using [Anaconda](https://www.anaconda.com/distribution/).

You'll first need to install conda if you haven't already. To then create and activate a new environment, run the following command:

```bash

conda create --name graphics python=3.10 -y
conda activate graphics

```

You'll then need to install the required packages by running:

```bash

pip install -r requirements.txt
pip install -e .

```
