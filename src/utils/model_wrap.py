import models
from sklearn.linear_model import LogisticRegression


def return_model(model_family='logistic', **kwargs):
    if model_family == 'logistic':
        solver = kwargs.get('solver', 'liblinear')
        n_jobs = kwargs.get('n_jobs', None)
        max_iter = kwargs.get('max_iter', 5000)
        model = LogisticRegression(solver=solver, n_jobs=n_jobs, 
                                   max_iter=max_iter, random_state=666)
    elif model_family == 'vit':
        model = models.ViTbp16(**kwargs)
    elif model_family == 'swin-tiny':
        model = models.SwinTiny(**kwargs)
    elif model_family == 'mobilenet':
        model = models.MobileNet(**kwargs)
    elif model_family == 'resnet-18':
        model = models.ResNet18(**kwargs)
    elif model_family == 'resnet-50':
        model = models.ResNet50(**kwargs)
    elif model_family == 'convnext-tiny':
        model = models.ConvNeXTTiny(**kwargs)
    return model
