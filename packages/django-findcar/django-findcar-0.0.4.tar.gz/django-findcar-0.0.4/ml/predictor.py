import numpy as np
import torch

from torchvision import datasets, models
from ml.util import process

# force matplotlib to not use Agg
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

# class to load the model and process images
class Predictor:
    # function to load model
    def load_model(self, checkpoint_path):
        # load the checkpoint and use cpu
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))

        # load resnet34 for transfer learning
        model = models.resnet34(pretrained=True)

        # get input features and classes
        num_input_features = model.fc.in_features
        model.class_to_idx = checkpoint['class_to_idx']
        num_classes = len(model.class_to_idx)

        # define the fully-connected layer to be a linear transformation from num_input_features to num_classes
        model.fc = torch.nn.Linear(num_input_features, num_classes)

        # load the weights from the checkpoint
        model.load_state_dict(checkpoint['state_dict'], strict=False)
    
        return model

    def __init__(self, checkpoint_path):
        # load model and use cpu
        self._model = self.load_model(checkpoint_path).cpu()
        self._classes = list(self._model.class_to_idx.keys())
    
    @property
    def classes(self):
        return self._classes

    '''
    function to predict the class of an image

    @params
    image_path = path to the image
    topk = how many of the top-predicted classes do you want returned

    @outputs
    pred_confs = np array of confidence values of predictions
    pred_classes = corresponding np aray of predicted class indexes
    '''
    def predict(self, image_path, topk=5):
        image = process.process_image(image_path)

        # convert image to float tensor and use cpu
        img_tensor = torch.from_numpy(image).type(torch.FloatTensor)
        img_tensor.cpu()

        # add a dimension to image to comply with (B x C x W x H) input of model
        img_tensor = img_tensor.unsqueeze_(0)

        # set model to evaluation mode and forward the image with gradients off
        self._model.eval()
        with torch.no_grad():
            output = self._model.forward(img_tensor)
 
        pred_confs = output.topk(topk)[0]
        pred_classes = output.topk(topk)[1]
        
        pred_confs = np.array(pred_confs)[0]
        pred_classes = np.array(pred_classes)[0]

        return pred_confs, pred_classes

    def plot_predictions(self, pred_confs, pred_classes, image_path):
        length = len(pred_classes)
        
        # convert classes to names and get prediction probabilities
        sum_confs = sum(pred_confs)
        pred_probs = []
        names = []
        for i in range(length):
            pred_probs.append(pred_confs[i] / sum_confs * 100)
            names.append(self._classes[pred_classes[i]])

        # create the plot
        plt.figure()
        plt.xlabel('Confidence Percentage')

        y_ticks = np.arange(len(names))
        plt.barh(y_ticks, pred_probs, color='blue')
        plt.yticks(y_ticks, names)
        plt.gca().invert_yaxis()
        
        plt.tight_layout()
        plt.savefig(image_path)
