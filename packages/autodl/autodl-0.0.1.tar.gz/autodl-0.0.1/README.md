# AutoDL Benchmark

A benchmark of AutoDL/AutoML methods to be run on the super-computer Jean Zay on ~100 datasets.

All AutoDL/AutoML/NAS algorithms will follow the same API and are run on [AutoDL datasets](https://autodl.lri.fr/competitions/162#learn_the_details-get_data). For `M` datasets and `N` algorithms, this benchmark will consist of a matrix of shape `M * N`, each entry being a performance score or a learning curve.

[Meeting minutes](https://docs.google.com/document/d/1RNEPXuUDynvlBLVDWvZHNFMHHnj1UGGAWgtQxtdSy08/edit?usp=sharing)

## Install

It is advised to create a virtual environment with `conda`:

```bash
conda create -n autodl python=3.7
conda activate autodl
```

Clone the repo and install with the `setup.py`:

```bash
git clone https://github.com/zhengying-liu/autodl-benchmark.git
cd autodl-benchmark/
pip install -e .
```

### Google Cloud

```bash

mkdir ~/autodl-project/
cd ~/autodl-project/
git clone https://github.com/zhengying-liu/autodl-benchmark.git
cd autodl-benchmark/
./install_miniconda.sh
cd
source ~/miniconda/bin/activate
conda create -n autodl python=3.7
conda activate autodl
cd autodl-project/autodl-benchmark/
pip install -e .
pip install -r requirements.txt
pip install torch==1.5.0+cu101 torchvision==0.6.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html
cd autodl/starting_kit/
python run_local_test.py -dataset_dir=../dataset/miniciao/ -code_dir=../../models/DARTS-AY/
```

### ALCF - Cooley

In `~/.soft.cooley` set:

```bash
+cuda-10.2
@default
```

```bash
export PATH="/soft/datascience/miniconda/bin:$PATH"
conda init bash
resoft
source ~/.bashrc
```

```bash
cd /projects/datascience/regele/
mkdir autodl-project
cd autodl-project/
conda create -p autodl-env python=3.7
ln -s $PWD/autodl-env ~/.conda/envs/autodl-env-cooley
conda activate autodl-env-cooley
git clone git@github.com:zhengying-liu/autodl-benchmark.git
cd autodl-benchmark/
pip3 install -r requirements.txt
```

### Test install

Try to import the package with python:

```bash
$ python
Python 3.7.5 (default, Oct 25 2019, 10:52:18)
[Clang 4.0.1 (tags/RELEASE_401/final)] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import autodl
>>> quit()
```

## Contributing

Using [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/).

## Dependencies

This repo is containing several machine learning algorithms. Each of the folder corresponds to a specific algorithm. For each algorithm you will find a `README.md` file containing instructions about how to use it and mostly how to get the required dependencies. For the dependencies, we will include a `requirement.txt` file to make it easier. A short reminder about this:

* How to create a `requirement.txt`?

```bash
pip freeze >> requirement.txt
```

* How to install packages from a `requirement.txt`?

```bash
pip install -r requirements.txt
```

## Run local test

```bash
python -m autodl.core.run -dataset_dir=../autodl/autodl/data/miniciao/ -code_dir=../autodl/workflows/Zero/ -score_dir=$PWD
```

## Detect GPU

In Pytorch:

```python
import torch
torch.cuda.is_available()
```

In Tensorflow:

```python
import tensorflow as tf
print(tf.test.is_gpu_available())
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
```

## Run Experiments on Google Cloud

1. type `screen` in the command line

2. Run your experiments

```console
$ cd path_to_autodl_repo/
$ ppython -m autodl.core.run -dataset_dir=../autodl/autodl/data/miniciao/ -code_dir=../autodl/workflows/Zero/ -score_dir=$PWD
```

3. Detach your session with Ctrl + A, Ctrl + D

4. You can quit whenever you want

5. Kill all detached screen with

```console
$ screen -ls | grep pts | cut -d. -f1 | awk '{print $1}' | xargs kill
```

## Download datasets

From shell:

```console
$ autodl dataset --name cifar10 --download
```

From Python:

```python
>>> from autodl.dataset.manager import AutoDLDataset
>>> hammer = AutoDLDataset(dataset_name='Hammer', download=True, dataset_dir="path/to/save")
```

## Execute benchmark

For debug:

```console
$ export MODELS_PATH="../autodl-benchmark/models/"
$ export MINICIAO_PATH="../autodl-benchmark/autodl/dataset/"
$ autodl bench --datasets miniciao --models LINEAR --datasets-path $MINICIAO_PATH --models-path $MODELS_PATH --budget 1200
```

For benchmark:

```console
$ export MODELS_PATH="../../autodl-benchmark/models/"
$ export DATASETS_PATH="../../autodl-benchmark/datasets/"
$ autodl bench --datasets cifar10 --models LINEAR --datasets-path $DATASETS_PATH --models-path $MODELS_PATH --budget 57600
```
