# Face Detection And Auto Crop
A python program that detects all human faces in an image and crops them automatically.

## Optional
The best practice for your project is to use a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

## Download
```
git clone https://github.com/nimon77/Face-Detection-And-Auto-Crop
```

## Python version: 3.11
You can use pyenv to have multiple python version on your system and make venv with pipenv

## Installation (with pipenv)
```
pip install --user pipenv
cd Face-Detection-And-Auto-Crop
pipenv install
pipenv shell
```

## Installation (with virtualenv)
```
cd Face-Detection-And-Auto-Crop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Installation (without virtualenv)
```
cd Face-Detection-And-Auto-Crop
pip install -r requirements.txt
```

## Usage
```
usage: auto_crop.py [-h] [-t THREAD] [-o OUTPUT] image [image ...]

Auto crop faces from images.

positional arguments:
  image                 image file or directory path

options:
  -h, --help            show this help message and exit
  -t THREAD, --thread THREAD
                        number of threads (default: 1)
  -o OUTPUT, --output OUTPUT
                        output directory (default: result)
```

## Example
```
python auto_crop.py images/peoples.jpg
```
or
```
python auto_crop.py image/peoples.jpg data/group.png human.jpeg
```
or
```
python auto_crop.py -t 4 images/
```
Successfully cropped images will be saved in a folder named "result" or in the output directory if specified
