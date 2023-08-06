# imagepreprocessing
##### A small library for speeding up the dataset preparation and model testing steps for deep learning on various frameworks. (mostly for me)
___

[![PyPI version fury.io](https://img.shields.io/pypi/v/imagepreprocessing?style=flat-square)](https://pypi.python.org/pypi/imagepreprocessing/) [![PyPI download month](https://img.shields.io/pypi/dw/imagepreprocessing?style=flat-square)](https://pypi.python.org/pypi/imagepreprocessing/) [![Downloads](https://pepy.tech/badge/imagepreprocessing)](https://pepy.tech/project/imagepreprocessing)
![](https://img.shields.io/github/repo-size/cccaaannn/imagepreprocessing?style=flat-square) [![GitHub license](https://img.shields.io/github/license/cccaaannn/imagepreprocessing?style=flat-square)](https://github.com/cccaaannn/imagepreprocessing/blob/master/LICENSE)

## What can it do
- **Creates all the required files for [darknet-yolo3,4](https://github.com/AlexeyAB/darknet) training including cfg file with default parameters and class calculations in a single line. ([example usage](#Create-required-files-for-training-on-darknet-yolo ))**
- **Creates train ready data for image classification tasks for keras in a single line.([example usage](#Create-training-data-for-keras))**
- **Makes multiple image prediction process easier with using keras model from both array and directory.**
- **Predicts and saves multiple images on a directory with using darknet.**
- **Includes a simple annotation tool for darknet-yolo style annotation. ([example usage](#Annotation-tool-for-derknet-yolo))**
- **Auto annotation by given random points for yolo.([example usage](#Create-required-files-for-training-on-darknet-yolo-and-auto-annotate-images-by-center ))**
- **Draws bounding boxes of the images from annotation files for preview.**
- **Plots training history graph from keras history object.([example usage](#Create-training-history-graph-for-keras))**
- **Plots confusion matrix.([example usage](#Make-prediction-from-test-array-and-create-the-confusion-matrix-with-keras-model))**

### This dataset structure is required for most of the operations 
```
my_dataset
   |----class1
   |     |---image1.jpg
   |     |---image2.jpg
   |     |---image3.jpg
   |     ...
   |----class2
   |----class3
         ...
```

## Install
```sh
pip install imagepreprocessing
```

## Create required files for training on darknet-yolo  
```python
from imagepreprocessing.darknet_functions import create_training_data_yolo
main_dir = "datasets/my_dataset"
create_training_data_yolo(main_dir)
```

## Create training data for keras
```python
from  imagepreprocessing.keras_functions import create_training_data_keras
source_path = "datasets/my_dataset"
save_path = "5000images_on_one_file"
train_x, train_y, valid_x, valid_y = create_training_data_keras(source_path, save_path = save_path, image_size = (299,299), validation_split=0.1, percent_to_use=0.5, grayscale = True)
```


## Make multiple image predictions from directory with keras model
```python
from  imagepreprocessing.keras_functions import make_prediction_from_directory_keras
predictions = make_prediction_from_directory_keras("datasets/my_dataset/class1", "models/alexnet.h5")
```

## Create training history graph for keras
```python
from  imagepreprocessing.keras_functions import create_history_graph_keras

# training
# history = model.fit(...)

create_history_graph_keras(history)
```
![trainig_histyory_example](readme_images/trainig_histyory_example.png)


## Make prediction from test array and create the confusion matrix with keras model
```python
from  imagepreprocessing.keras_functions import create_training_data_keras, make_prediction_from_array_keras
from  imagepreprocessing.utilities import create_confusion_matrix, train_test_split

images_path = "datasets/my_dataset"

# Create training data split the data
x, y, x_val, y_val = create_training_data_keras(images_path, save_path = None, validation_split=0.2, percent_to_use=0.5)

# split training data
x, y, test_x, test_y =  train_test_split(x,y,save_path = save_path)

# ...
# training
# ...

class_names = ["apple", "melon", "orange"]

# make prediction
predictions = make_prediction_from_array_keras(test_x, model, print_output=False)

# create confusion matrix
create_confusion_matrix(predictions, test_y, class_names=class_names, one_hot=True)
create_confusion_matrix(predictions, test_y, class_names=class_names, one_hot=True, cmap_color="Blues")
```
![confusion_matrix_example](readme_images/confusion_matrix_example1.png)![confusion_matrix_example](readme_images/confusion_matrix_example2.png)


## Make multi input model prediction and create the confusion matrix
```python
from imagepreprocessing.keras_functions import create_training_data_kera
from  imagepreprocessing.utilities import create_confusion_matrix, train_test_split
import numpy as np

# Create training data split the data and split the data
source_path = "datasets/my_dataset"
x, y = create_training_data_keras(source_path, image_size=(28,28), validation_split=0, percent_to_use=1, grayscale=True, convert_array_and_reshape=False)
x, y, test_x, test_y = train_test_split(x,y)

# prepare the data for multi input training and testing
x1 = np.array(x).reshape(-1,28,28,1)
x2 = np.array(x).reshape(-1,28,28)
y = np.array(y)
x = [x1, x2]

test_x1 = np.array(test_x).reshape(-1,28,28,1)
test_x2 = np.array(test_x).reshape(-1,28,28)
test_y = np.array(test_y)
test_x = [test_x1, test_x2]

# ...
# training
# ...

# make prediction
predictions = make_prediction_from_array_keras(test_x, model, print_output=False, model_summary=False, show_images=False)

# create confusion matrix
create_confusion_matrix(predictions, test_y, class_names=["0","1","2","3","4","5","6","7","8","9"], one_hot=True)

```


## Create required files for training on darknet-yolo and auto annotate images by center 
##### Auto annotation is for testing the dataset or just for using it for classification, detection won't work without proper annotations.
```python
from imagepreprocessing.darknet_functions import create_training_data_yolo, auto_annotation_by_random_points
import os

main_dir = "datasets/my_dataset"

# auto annotating all images by their center points (x,y,w,h)
folders = sorted(os.listdir(main_dir))
for index, folder in enumerate(folders):
    auto_annotation_by_random_points(os.path.join(main_dir, folder), index, annotation_points=((0.5,0.5), (0.5,0.5), (1.0,1.0), (1.0,1.0)))

# creating required files
create_training_data_yolo(main_dir)
```


## Annotation tool for derknet-yolo
```python
from imagepreprocessing.darknet_functions import yolo_annotation_tool
yolo_annotation_tool("test_stuff/images", "test_stuff/obj.names")
```
