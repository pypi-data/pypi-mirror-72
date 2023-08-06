import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from .dnn import DNN
from .multidnn import MultiDNN

__version__ = "0.5.0a2"

def subprocess (train_func, *args):
    from multiprocessing import Pool
    with Pool(1) as p:
        return p.apply (train_func, args)
