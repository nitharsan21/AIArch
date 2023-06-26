import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from tensorflow_addons.layers import InstanceNormalization

from mlgan.core import data_sources, preprocessing

log = logging.getLogger(__name__)


class BaseGenerator:


    def __init__(self, model_location, categories, input_shape):
        #Initialize the generator with a model.


        self._model = {}

        self.model_type = None

        self.input_shape = input_shape
        self.model_location = Path(model_location)
        self.categories = categories

    def load_model(self, model_location=None):
        #Load the generator model.

        model_location = model_location if model_location else self.model_location

        for _cat in self.categories:
            log.info(f"Loading model for category: {_cat}.")
            self._model[_cat] = load_model(
                model_location / _cat / "generator.h5",
                compile=False,
                custom_objects={"Addons>InstanceNormalization": InstanceNormalization},
            )

    def preprocess_image(self, img):

        preprocessed_img = preprocessing.resize_and_pad(
            img, size=(self.input_shape[0], self.input_shape[1]), pad_color=255
        )
        preprocessed_img = data_sources.normalize_image(preprocessed_img)
        return preprocessed_img

    def visualize_predictions(self, img, predictions):
        preprocessed_img = self.preprocess_image(img)
        preprocessed_img = (preprocessed_img * 0.5) + 0.5
        n_predictions = len(predictions.keys())

        fig, axes = plt.subplots(
            figsize=(15, 3 * n_predictions),
            nrows=int(np.ceil((n_predictions + 1) / 3)),
            ncols=3,
        )
        input_results = [preprocessed_img] + list(predictions.values())
        titles = ["input"] + [
            f"{comb[0]}_{comb[1]}" for comb in list(predictions.keys())
        ]

        i = 0
        for title, img, ax in zip(titles, input_results, axes.flatten()):
            # plt.subplot(ax)
            plt.title(f"{i}_{title}", fontweight="bold")
            plt.imshow(img)
            plt.axis("off")
            i += 1
            plt.show()

        for ax in axes.flatten():
            # plt.subplot(ax)
            plt.axis("off")
        plt.tight_layout()
        plt.show()
        return fig, axes

    def predict(self):

        raise NotImplementedError

    def postprocess_predictions(self):

        raise NotImplementedError

