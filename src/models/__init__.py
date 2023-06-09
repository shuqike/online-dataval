# from src.models.pt_cnn import MobileNet, ResNet18, ResNet50, ConvNeXTTiny, LeNet10, LeNet100, LeNetMNIST, R9Cifar10, ReallySimple
# from src.models.pt_vit import ViTbp16, SwinTiny
# from src.models.classifier import Lancer
from src.models.ensemble_DV_core import RandomForestClassifierDV, RandomForestRegressorDV
from src.models.bagging_DV_core import BaggingClassifierDV, BaggingRegressorDV
from src.models.value_nn import Vestimator, Vestimator_1, ResVestimatorMNIST, R18VestimatorMNIST, LeVestimatorMNIST