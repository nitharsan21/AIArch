import logging

import numpy as np

from mlgan.generator.BaseGenerator import BaseGenerator
from mlgan.core import utils

log = logging.getLogger(__name__)


class BaseBiCycleGAN(BaseGenerator):


    def __init__(self, model_location, categories, input_shape, latent_vector=8):

        super().__init__(model_location, categories, input_shape)
        self.latent_vector = latent_vector

    def predict(self, img, n_samples, z_random=None, categories=None):

        categories = categories if categories else self.categories
        preprocessed_img = self.preprocess_image(img)
        preprocessed_img = np.reshape(
            preprocessed_img,
            (1, self.input_shape[0], self.input_shape[1], self.input_shape[2]),
        )

        predictions = {}
        for _cat in categories:
            for i in np.arange(n_samples):
                noise = (
                    z_random if z_random else utils.create_z_random(self.latent_vector)
                )
                _pred = self._model[_cat].predict([preprocessed_img, noise])
                _pred = (_pred * 0.5) + 0.5
                predictions[(_cat, i)] = _pred[0]
        return predictions

    def postprocess_predictions(self, predictions, input_img):

        raise NotImplementedError
