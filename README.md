# Image analysis toolbox in Python

## Installation for development

Make sure you use Python 3.8 `python -V`

Otherwise:

```
conda create -n ia python=3.8
conda activate ia
```

or download and install Python 3.8

Install the package in development mode.
```
git clone git@gitlab.pasteur.fr:pub/image-analysis.git
cd image-analysis
pip install -e .
pip install -r requirements.txt
```

## How to contribute

Commit your changes into separate branch with clear name of what's intended to be done.

Write clean code. Supply functions with types, default arguments and doc strings.

Every function should have  unit tests.

Update documentation with new functionality.

Once your code meets the goal and all test are passing, make a pull request.

## API

### Pre-processing

If analysing the images from image stacks, it is necessary to rename the files specifically as `cXmYtZ.tiff` (example `c1m03t121.tiff`). All the images need to be stored in a unique folder `FOLDER`.

Direct analysis from `.nd2` files will be released soon.

### Image analysis

In the terminal enter:

`python -m track_ot1 FOLDER`

and enjoy.
```
