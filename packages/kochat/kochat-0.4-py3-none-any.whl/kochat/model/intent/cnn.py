"""
@author : Hyunwoong
@when : 5/11/2020
@homepage : https://github.com/gusdnd852
"""
import torch
from torch import nn
from torch import Tensor
from kochat.decorators import intent
from kochat.model.convolution import Convolution


@intent
class CNN(nn.Module):

    def __init__(self, label_dict: dict, residual: bool = True):
        """
        Intent Classification을 위한 CNN 클래스입니다.

        :param label_dict: 라벨 딕셔너리
        :param residual: skip connection 여부
        """

        super(CNN, self).__init__()
        self.label_dict = label_dict
        self.stem = Convolution(self.vector_size, self.d_model, kernel_size=1, residual=residual)
        self.hidden_layers = nn.Sequential(*[
            Convolution(self.d_model, self.d_model, kernel_size=1, residual=residual)
            for _ in range(self.layers)])

        # distance => DistanceIntentClassifier
        self.distance_features = nn.Linear(self.d_model * self.direction, self.d_loss)
        self.distance_classifier = nn.Linear(self.d_loss * self.direction, len(self.label_dict))

        # softmax => SoftmaxIntentClassifier
        self.softmax_classifier = nn.Linear(self.d_model, len(self.label_dict))

    def forward(self, x: Tensor) -> Tensor:
        x = x.permute(0, 2, 1)
        x = self.stem(x)
        x = self.hidden_layers(x)
        x = x.view(x.size(0), -1)
        return x
