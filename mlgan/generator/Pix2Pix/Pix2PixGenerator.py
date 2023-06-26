import logging

import numpy as np

from mlgan.generator.Pix2Pix import BasePix2Pix

log = logging.getLogger(__name__)


class Pix2PixGenerator(BasePix2Pix):


    def __init__(self, model_location, categories, conf_location):
        super().__init__(model_location, categories, conf_location)
        self.model_type = "Pix2Pix"

        self.load_configuration()
        self.load_model()

    def predict(self, img, n_samples, categories=None):
        categories = categories if categories else self.categories
        preprocessed_img = self.preprocess_image(img)
        preprocessed_img = np.reshape(
            preprocessed_img,
            (1, self.input_shape[0], self.input_shape[1], self.input_shape[2]),
        )

        predictions = {}
        for _cat in categories:
            for i in np.arange(n_samples):
                _pred = self._model[_cat].predict(preprocessed_img)
                _pred = (_pred * 0.5) + 0.5
                predictions[(_cat, i)] = _pred[0]
        return predictions
