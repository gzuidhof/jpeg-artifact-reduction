from __future__ import division
import numpy as np

import keras
from keras.engine.topology import Layer
from keras.layers import Input, merge, Convolution2D, MaxPooling2D, AveragePooling2D, Deconvolution2D
from keras import backend as K

import dct

class SubSampleLayer(Layer):
    def __init__(self, factor=8, **kwargs):
        self.factor = factor
        super(SubSampleLayer, self).__init__(**kwargs)

    def call(self, x, mask=None):
        return x[:,:,::self.factor,::self.factor]

    def get_output_shape_for(self, input_shape):
        return (input_shape[0], input_shape[1], input_shape[2]//self.factor, input_shape[3]//self.factor)


class QuantizationLayer(Layer):
    def __init__(self, Q=None, unquantization=False, quality_factor=50, **kwargs):
        self.Q = Q
        self.unquantization = unquantization
        self.quality_factor = quality_factor
        
        super(QuantizationLayer, self).__init__(**kwargs)
    
    def build(self, input_shape):
        if self.Q is None:
            Ts = dct.quantization_matrix(self.quality_factor)
            Ts = Ts[:, np.newaxis, np.newaxis]
            
            # improvement: use broadcasting instead
            self.Q = K.repeat_elements(K.repeat_elements(
                K.variable(value=
                    Ts, dtype='float32'), input_shape[2], 1), input_shape[3], 2)
        
        super(QuantizationLayer, self).build(input_shape)
    
    def call(self, x, mask=None):
        if self.unquantization:
            return x*self.Q
        else:
            return K.round((x)/self.Q)
        
    def get_output_shape_for(self, input_shape):
        return input_shape

def _onehot_weights():
    patcher_weights = np.zeros((64,1,8,8), dtype=np.float32)
    for x in range(64):
        patcher_weights[x, 0, 7-x//8, 7-x%8] = 1.
    return patcher_weights


def to_dct_layers(in_layer, R=8):
    patcher = Convolution2D(64, 8, 8, border_mode='valid',
                            weights=[_onehot_weights()],
                            trainable=False,
                            subsample=(8//R,8//R),
                            bias=False)(in_layer)

    dct_l = Convolution2D(64, 1, 1, border_mode='same', 
                            weights = [np.expand_dims(np.expand_dims(dct.dct_weights(), 2),2)],
                            trainable=False,
                            bias=False)(patcher)

    return dct_l
           
def to_pixel_layers(in_layer, R=8, restore_size=128):
    #pooly = SubSampleLayer(R)(in_layer)

    dcti_l = Convolution2D(64, 1, 1, border_mode='same', 
                            weights = [np.expand_dims(np.expand_dims(dct.dct_weights().T, 2),2)],
                            trainable=False,
                            bias=False)(in_layer)

    unpatcher = keras.layers.Deconvolution2D(1, 8, 8,
                            output_shape=(None,1,restore_size,restore_size), subsample=(8,8), border_mode='valid', 
                            weights=[_onehot_weights().transpose(1,0,2,3)], 
                            trainable=False,
                            bias=False)(dcti_l)

    return unpatcher