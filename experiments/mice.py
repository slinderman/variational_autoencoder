import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
import gzip
import logging
import logging.config
logging.config.fileConfig('logging.conf')

from vae.vae import make_gaussian_fitter
from vae.optimization import sgd, adagrad, rmsprop, adadelta, adam, \
    momentum_sgd, nesterov
from vae.util import get_ndarrays

from load import load_mice


if __name__ == '__main__':
    logging.info('\n\nStarting experiment!')
    np.random.seed(0)

    N = 750000  # 750k is about the memory limit on 3GB GPU
    trX = load_mice(N)

    encoder_params, decoder_params, fit = \
        make_gaussian_fitter(trX, 20, [200, 200], [200, 200])

    fit(1, 50, 1, adadelta())
    fit(1, 250, 1, adadelta())
    fit(10, 500, 1, rmsprop(1e-4))
    fit(25, 500, 1, rmsprop(1e-5))
    fit(25, 1000, 1, rmsprop(1e-5))

    params = get_ndarrays(encoder_params), get_ndarrays(decoder_params)
    with gzip.open('params.pkl.gz', 'w') as f:
        pickle.dump(params, f, protocol=-1)
