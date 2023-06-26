from mlgan.generator.run import run as build_generator
from mlgan.core import preprocessing, postprocessing, data_sources
from pathlib import Path
import random
import logging
import os
import numpy as np
import cv2
import ast
import matplotlib.pyplot as plt


os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    input_images = Path('../data/images/complete_floorplan/input/377.png')

    config = '../config/generator/complete_floorplan.yaml'


    config = data_sources.load_yaml(Path("../config/generator/complete_floorplan.yaml"))
    config["settings"]["input_shape"] = ast.literal_eval(
        config["settings"]["input_shape"]
    )

    generator = build_generator(config)

    # input_images_list = [x for x in input_images.glob('*.png')]
    # print(len(input_images_list))


    random_file = Path('../data/images/complete_floorplan/input/49.png')

    input_image = cv2.imread(str(random_file))
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    predictions = generator.predict(input_image, 5)

    generator.visualize_predictions(input_image, predictions=predictions)

    postprocessed_predictions = generator.postprocess_predictions(predictions=predictions, input_img=input_image)

    preprocessed_img = preprocessing.resize_and_pad(
        input_image, size=(256, 256), pad_color=255
    )

    in_img_gdf = preprocessing.image_to_geodataframe(preprocessed_img)
    in_img_gdf.geometry = [in_img_gdf.unary_union] * in_img_gdf.shape[0]
    in_img_gdf = in_img_gdf.head(1).explode().reset_index(drop=True)

    n_predictions = len(postprocessed_predictions.keys())
    fig, axes = plt.subplots(nrows=int(np.ceil(n_predictions / 2)), ncols=2, figsize=(30, 30))
    axes = axes.flatten()
    for _preds, ax in zip(postprocessed_predictions.items(), axes):
        in_img_gdf.exterior.buffer(1).plot(ax=ax, color='black')

        _key, _res = _preds
        _res.plot(color=_res['colors'], ax=ax)
        _res.exterior.plot(color='black', ax=ax)
        ax.set_title(_key)

    for ax in axes:
        ax.axis('off')
    fig.suptitle('Postprocessed floorplans', fontsize=16, y=1)
    plt.tight_layout()
    plt.show()