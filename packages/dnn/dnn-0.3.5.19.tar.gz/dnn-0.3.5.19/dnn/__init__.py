from .dnn import DNN
from .multidnn import MultiDNN

__version__ = "0.3.5.19"

def subprocess (train_func, *args):
    from multiprocessing import Pool
    with Pool(1) as p:
        return p.apply (train_func, args)

