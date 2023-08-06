# Setup
1. Make a virtual Python environment
2. `pip install -r requirements.txt`

# Use
- `cd ml && python3 predict.py PATH-TO-IMAGE`
  - For example, `cd ml && python3 predict.py test/images/2012-mercedes-benz-e350-fd.jpg`
- python3 `get_classes.py` is to get the classes ist and classes to index dict from the dataset
  - For example, `cd ml/util && python3 get_classes.py ../../stanford-car-dataset-by-classes/car_data/train`
  - It will save these as JSON objects: `classes.json` and `class_to_idx.json`

# Notebooks and Training the Model
- Model training is done within the notebooks (.ipynb files)
- To open these:
  1. `pip install notebook`
  2. `jupyter notebook`
  3. Browse to the notebooks
  - or open them in Google colab or with the `VSCode Jupyter Notebook` extension
- You will need the [stanford cars dataset by classes](https://www.kaggle.com/jutrera/stanford-car-dataset-by-classes-folder)
- Upload your model to the Google Drive, NOT GitHub (we may change this to use LFS)