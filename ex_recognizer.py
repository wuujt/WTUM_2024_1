import os
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

model = models.resnet50(weights=None)
w = torch.load('animals.pth', map_location=torch.device('cpu'))
model_state_dict = w['model_state_dict']
class_labels = w['class_labels']
model.load_state_dict(model_state_dict)
model.eval()

data_transform = transforms.Compose([
    transforms.Resize(224), 
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
image_path = os.path.abspath('datasets/test/squirrel/OIP-0GZlVDOLvJ6v3ypXwXcykQHaEK.jpeg')
image = Image.open(image_path)
image = data_transform(image)
image = image.unsqueeze(0)

with torch.no_grad():
    outputs = model(image)

_, predicted = torch.max(outputs, 1)
index = predicted.item()

predicted_class = class_labels[index]
print('observed -', predicted_class)