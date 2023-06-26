import logging

from mlgan.core import postprocessing
from mlgan.generator.BiCycleGAN import BaseBiCycleGAN

log = logging.getLogger(__name__)


class BiCycleGANGenerator(BaseBiCycleGAN):


    def postprocess_predictions(self, predictions, input_img):
        processed_results = {}
        for key, _pred in predictions.items():
            cleaned_gdf = postprocessing.postprocess_prediction(input_img, _pred)
            processed_results[key] = cleaned_gdf
        return processed_results
