import torch.nn as nn
import torchvision.models as models


def get_model(num_classes: int = 10):
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model
