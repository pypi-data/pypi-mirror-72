import sys

# allow imports from root
sys.path.append('..')

from ml import predictor

checkpoint_path = 'model/checkpoint.pth'

if (len(sys.argv) != 2):
    print('Expected 1 argument: image_path')
    sys.exit()
image_path = sys.argv[1]

predictor = predictor.Predictor(checkpoint_path)

classes = predictor.classes

num_classes = len(classes)
print(f'{num_classes} classes')

# optionally, pass in topk=?
pred_confs, pred_classes = predictor.predict(image_path, topk=10)

print('Predicted Confidences')
print(pred_confs)
print('Predicted Classes')
print(pred_classes)
print('Top Predicted Class')
print(classes[pred_classes[0]])

plot_image_path = 'plot.png'
predictor.plot_predictions(pred_confs, pred_classes, plot_image_path)

print(f'Confidence plot saved to {plot_image_path}')
