![](https://img.shields.io/badge/python-3.8-blue)

# TakeConfunsionMatrix 
TakeConfusionMatrix is a Python package for batched Machine Learning metrics calculation and is distributed under MIT License.

## Goal
The main goal of this package is to enable calculation of Machine Learning metrics for hundreds of milions of results through batch computation.

## Features
The current package features are:
- Confusion Matrix 
    - Image output
    - Normalized output
    - Custom labelled output
- Precision Score
- Recall Score
- F1-Score
- Accuracy Score (Exact Match Ratio)

## Installation
### Dependencies
TakeConfusionMatrix requires:
- Python (>= 3.8)
- Pandas (>= 1.0.4)
- scikit-learn (>= 0.23.1)

### User installation
Install the 64bit version of Python, for instance from https://www.python.org/. Then run:

```bash
pip install -U TakeConfusionMatrix
```

### VirutalEnv installation
In order to avoid potential conflicts with other packages it is strongly recommended to use a virtual environment, e.g. python3 `virtualenv` (see [python3 virtualenv documentation](https://docs.python.org/3/tutorial/venv.html)) or conda environments. 

To do so, install the 64bit version of Python3 if you doesn't have it yet, then run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U TakeConfusionMatrix
```

**NOTE**: Please note that the above instructions assume a Linux-based SO. If you are using another environment, see [scikit-learn installation documentation](https://scikit-learn.org/stable/install.html).

## Usage
Here the package's features are briefly presented. For more advanced examples, please refer to the methods documentation.

### Matrix computation
```python
# Import MetricsComputation class
from take_confusion_matrix import MetricsCalculation

# Initialize class
labels = [0, 1, 2]
mc = MetricsCalculator(labels)

# Compute matrix
y_true = [0, 1, 0, 1]
y_pred = [0, 0, 0, 0]
mc.compute_matrix(y_true, y_pred)

y_true = [0, 2, 0, 2]
y_pred = [0, 0, 0, 0]
mc.compute_matrix(y_true, y_pred)

# Generate matrix
confusion_matrix = mc.generate_confusion_matrix()
print(confusion_matrix)
```

#### Normalized matrix
```python
confusion_matrix = mc.generate_confusion_matrix(normalize=True)
```

#### Custom labelled matrix
```python
labels = ["class_0", "class_1", "class_2"]
confusion_matrix = mc.generate_confusion_matrix(labels=labels)
```

#### Label free matrix
```python
confusion_matrix = mc.generate_confusion_matrix(with_labels=False)
```

#### Image matrix
```python
mc.generate_confusion_matrix(as_image=True)
```

### Metrics computation
```python
# Import MetricsComputation class
from take_confusion_matrix import MetricsCalculation

# Initialize class
labels = [0, 1, 2]
mc = MetricsCalculator(labels)

# Compute matrix
y_true = [0, 1, 0, 1]
y_pred = [0, 0, 0, 0]
mc.compute_matrix(y_true, y_pred)

y_true = [0, 2, 0, 2]
y_pred = [0, 0, 0, 0]
mc.compute_matrix(y_true, y_pred)

# Generate metics
metrics = mc.generate_metrics()
print(metrics)
```

## Testing
In order to test package's features, you must download the code and change you current directory (cd) to the package's one. After that, open a terminal inside package's folder and type:

```bash
pytest
```

All tests are stored inside `tests` folders, meaning that any test folder named `tests` contains a test set.

## Maintainer
Take's D&A Team | [analytics.ped@take.net](mailto:analytics.ped@take.net)

## Author
Cecília Regina Oliveira de Assis | [@ceciliassis](https://github.com/ceciliassis)
