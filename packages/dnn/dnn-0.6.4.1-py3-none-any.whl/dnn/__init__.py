__version__ = "0.6.4.1"

def subprocess (train_func, *args):
    from multiprocessing import Pool
    with Pool(1) as p:
        return p.apply (train_func, args)
