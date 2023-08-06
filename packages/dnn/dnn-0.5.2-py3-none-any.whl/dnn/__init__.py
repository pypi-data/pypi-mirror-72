import tensorflow as tf
if tf.__version__ [0] == '2':
    import warnings
    warnings.warn ("dnn use tf.compat.v1.disable_v2_behavior ()", DeprecationWarning)
    tf.compat.v1.disable_v2_behavior ()

from .dnn import DNN
from .multidnn import MultiDNN

__version__ = "0.5.2"

def subprocess (train_func, *args):
    from multiprocessing import Pool
    with Pool(1) as p:
        return p.apply (train_func, args)
