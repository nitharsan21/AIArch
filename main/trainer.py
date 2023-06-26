import argparse
import logging
import os

import tensorflow as tf

from mlgan import trainer
from mlgan.core import labeling, data_sources

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
)
log = logging.getLogger(__name__)


def show_model_categories():

    log.info("The model categories are:")
    for _cat in labeling.MODEL_CATEGORIES:
        log.info(f"{_cat}")
    log.info(
        "To create a model that predicts the inverse of a category, prepend the categeroy "
        f'with  "no_", such as no_{labeling.MODEL_CATEGORIES[0]}.'
    )


def main(args):
    #Main function that serves as an entry point for the neural network training jobs.

    conf_options = data_sources.load_yaml(args.config)

    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    if not conf_options["settings"]["use_gpu"]:
        # os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        log.info("GPU usage has been turned off.")
    else:
        log.info(f'Available GPU devices: {tf.config.list_physical_devices("GPU")}')

    tf.autograph.set_verbosity(0)

    if args.category:
        log.info(f"Updating with new category: {args.category}")
        conf_options["settings"]["category"] = args.category

    trainer.run(conf_options)


if __name__ == "__main__":
    # config = '../config/trainer/config_nn_floor_plan.yaml'
    # config = '../config/trainer/config_nn_structure_plan.yaml'
    config = '../config/trainer/config_nn_complete_floorplan.yaml'

    show_model_categories()

    parser = argparse.ArgumentParser(description="Train a neural_network.")
    parser.add_argument(
        "--config", type=str, metavar="config", help="Path to the config location.",
        default= config,
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        metavar="category",
        help="model dataset category. Will overwrite config value.",
    )

    args = parser.parse_args()
    main(args)
