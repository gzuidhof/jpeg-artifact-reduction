import numpy as np

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
        from http://goo.gl/DZNhk
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def onehot_weights():
    patcher_weights = np.zeros((64,1,8,8), dtype=np.float32)
    for x in range(64):
        patcher_weights[x, 0, 7-x//8, 7-x%8] = 1.
    return patcher_weights

def center_crop(layer, target_size):
        batch_size, n_channels, layer_width, layer_height = layer.size()
        w = (layer_width - target_size[0]) // 2
        h = (layer_height - target_size[1]) // 2
        return layer[:, :, w:(w + target_size[0]), h:(h + target_size[1])]
