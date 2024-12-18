import os
import threading
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image


class I2v:
  cuda_core = "cuda:0" if "CUDA_ENABLE" in os.environ else "cpu"

  def __init__(self):
    self.device = torch.device(self.cuda_core)

    self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    self.layer_output_size = 2048
    self.extraction_layer = self.model._modules.get('avgpool')

    self.model = self.model.to(self.device)

    self.model.eval()

    self.scaler = transforms.Resize((224, 224))
    self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                          std=[0.229, 0.224, 0.225])
    self.to_tensor = transforms.ToTensor()
    self.lock = threading.Lock()

  def get_vector(self, image) -> list:
    img = Image.open(image).convert('RGB')

    with self.lock:
      image = self.normalize(self.to_tensor(self.scaler(img))).unsqueeze(0).to(self.device)
      my_embedding = torch.zeros(1, self.layer_output_size, 1, 1)

      def copy_data(*args):
        my_embedding.copy_(args[2].data)

      h = self.extraction_layer.register_forward_hook(copy_data)
      self.model(image)
      h.remove()

      return my_embedding.numpy()[0, :, 0, 0].tolist()
    

i2v = I2v()
