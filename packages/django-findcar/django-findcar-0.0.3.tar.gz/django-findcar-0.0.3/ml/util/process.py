from PIL import Image
import numpy as np
import torch
from torchvision import datasets, transforms

# to use with imagenet trained NNs
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

DEFAULT_MEAN = (0.5, 0.5, 0.5)
DEFAULT_STD = (0.5, 0.5, 0.5)

 # downsize image res to 256, crop the center 224, and grayscale
PREPROCESS_TRANSFORM = transforms.Compose([
    transforms.Resize((244, 244)),
    transforms.ToTensor(),
    transforms.Normalize(DEFAULT_MEAN, DEFAULT_STD)
])

# preprocess and rotate and flip images for more data
DATA_AUGMENT_TRANSFORM = transforms.Compose([
    transforms.Resize((244, 244)),
    # careful with random rotations, they keep zeroing out the tensor...
    # transforms.RandomRotation(10),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(DEFAULT_MEAN, DEFAULT_STD)
])

# process the image in the same way as our training data
def process_image(image_path):
    image = Image.open(image_path)
    
    transformed_image = PREPROCESS_TRANSFORM(image)
    array = np.array(transformed_image)
    
    return array
