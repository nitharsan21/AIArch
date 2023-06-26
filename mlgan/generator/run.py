import logging

from mlgan.generator.BiCycleGAN import SingleStepGenerator

log = logging.getLogger(__name__)


def run(config):
    generator = SingleStepGenerator(
        model_location=config["settings"]["models_directory"],
        input_shape=config["settings"]["input_shape"],
        categories=config["settings"]["categories"],
    )
    generator.load_model()

    return generator
