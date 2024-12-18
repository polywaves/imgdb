#!/usr/bin/env python3

import torchvision.models as models


models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
