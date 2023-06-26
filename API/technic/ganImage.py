from mlgan.generator.run import run as build_generator
from mlgan.core import preprocessing, postprocessing, data_sources
from pathlib import Path
import uuid
import logging
import os
import numpy as np
import cv2
import ast
import matplotlib.pyplot as plt
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


def ganFloorPlan(generator, data):

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    input_images = Path('../API/' + data['image'])

    input_image = cv2.imread(str(input_images))

    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    predictions = generator.predict(input_image, 3)

    generator.visualize_predictions(input_image, predictions=predictions)

    urls = save_predictions(generator, input_image, predictions)

    return urls




def save_predictions(generator, img, predictions):
    # Save the predictions images
    preprocessed_img = generator.preprocess_image(img)
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

    image_urls = []  # List to store the URLs of the saved images

    i = 0
    for title, img, ax in zip(titles, input_results, axes.flatten()):
        plt.imshow(img)
        plt.axis("off")
        i += 1
        # Generate a unique filename for the image
        filename = f"{str(uuid.uuid4())}.png"
        filepath = os.path.join("../API/static/image/predictions", filename)

        # Save the image
        plt.savefig(filepath)
        plt.close()

        # Append the URL of the saved image to the list
        image_url = f"/static/image/predictions/{filename}"
        image_urls.append(image_url)

    plt.tight_layout()

    return image_urls