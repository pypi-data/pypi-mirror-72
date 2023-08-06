import tensorflow as tf
if tf.__version__ [0] == '2':
    tf.compat.v1.disable_v2_behavior ()
from .dnn import DNN
from .multidnn import MultiDNN

__version__ = "0.6.3.1"
def subprocess (train_func, *args):
    from multiprocessing import Pool
    with Pool(1) as p:
        return p.apply (train_func, args)
