import argparse
import ast
import logging

from mlgan.core import data_sources
from mlgan.generator import run

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
)
log = logging.getLogger(__name__)


def build_bicyclegan_generator(config):
    #Build a generator interface model.
    log.info("Loading model...")
    model = run.run(config)
    log.info("Model loaded successfully!")
    return model


if __name__ == "__main__":
    config = '../config/generator/complete_floorplan.yaml'

    parser = argparse.ArgumentParser(description="Train a neural_network.")
    parser.add_argument(
        "--config", type=str, metavar="config", help="Path to the config location.",
        default=config,
    )
    args = parser.parse_args()

    config = data_sources.load_yaml(config_location=args.config)
    config["settings"]["input_shape"] = ast.literal_eval(
        config["settings"]["input_shape"]
    )

    build_bicyclegan_generator(config)
