# VidTrain

Train deep neural networks to analyze video data.

## Installation

1. [Install anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. (Optional) Install a python-capable IDE like [Visual Studio Code](https://code.visualstudio.com/)
3. Open a command line terminal to install `vidtrain`: 
   1. Create a python 3.7 environment: `conda create --name vidtrain python=3.7`. Note, the python version must be exactly 3.7 [[1]](#Notes)
   2. Activate the environment `conda activate vidtrain`
   3. Install vidtrain `pip install vidtrain`
   
## Run

Execute the following code in python:
```python
import vidtrain


if __name__ == '__main__':
    vidtrain.workflow.JunctionAnalysis().run()
```


## Notes
[1]  The code uses some features that were introduced in 3.7 (dictionaries that are ordered by default), meaning it will not work properly with python <3.7. Furthermore, it uses Tensorflow 1 , which dpes not support 3.8. Thus, the python version must be *exactly* 3.7. In the future, it is planned to migrate to Tensorflow 2 and at that point, vidtrain will also work on python 3.8. However, this will require rewriting at least the data generator for the validation data.