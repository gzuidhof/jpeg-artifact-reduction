from __future__ import division
import numpy as np
from keras import backend as K

def PSNRLoss_scaled(y_true, y_pred):
    """
    PSNR is Peek Signal to Noise Ratio, which is similar to mean squared error.
    It can be calculated as
    PSNR = 20 * log10(MAXp) - 10 * log10(MSE)
    When providing an unscaled input, MAXp = 255. Therefore 20 * log10(255)== 48.1308036087.
    However, since we are scaling our input, MAXp = 1. Therefore 20 * log10(1) = 0.
    Thus we remove that component completely and only compute the remaining MSE component.
    """
    return -10. * np.log10(K.mean(K.square(y_pred - y_true)))

def PSNRLoss(y_true, y_pred):
    # 20*log10(255)
    return 48.1308036087 - (10. * np.log10(K.mean(K.square(y_pred - y_true))))

def psnr(y_true, y_pred):
    #assert y_true.shape == y_pred.shape, "Cannot calculate PSNR. Input shapes not same." \
    #                                     " y_true shape = %s, y_pred shape = %s" % (str(y_true.shape),
    #                                                                               str(y_pred.shape))
    
    # 20*log10(255)
    return 48.1308036087 - (10. * np.log10(np.mean(np.square(y_pred - y_true))))
    