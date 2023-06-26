import logging
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm

from mlgan.core import preprocessing, data_sources, labeling

log = logging.getLogger(__name__)


def split(a, n):

    n = min(n, len(a))
    k, m = divmod(len(a), n)
    return [a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)]


class GeoDataGenerator:


    def __init__(self, input_directory, output_directory):

        self.input_directory = Path(input_directory)
        self.output_directory = Path(output_directory)

        self.output_directory.mkdir(parents=True, exist_ok=False)

    def save_block(self, dataset, dataset_block):

        dataset_gdf = pd.concat(dataset)
        dataset_gdf["original_file"] = dataset_gdf["original_file"].astype(str)

        dataset_gdf.to_file(
            str(self.output_directory / f"floorplans_{dataset_block}.json"),
            driver="GeoJSON",
        )

    def generate_single_example(self, filename):
        (
            walls_gdf,
            doors_gdf,
            rooms_gdf,
            special_gdf,
        ) = data_sources.parse_floorplan_txt(filename)
        colormap = labeling.get_room_color_map()

        floorplan_gdf = preprocessing.create_floorplan_gdf(
            walls_gdf, doors_gdf, rooms_gdf, special_gdf, colormap
        )
        floorplan_gdf["original_file"] = filename.absolute()

        index_single_example = preprocessing.calculate_room_counts(floorplan_gdf)
        index_single_example["original_file"] = str(filename.absolute())
        return floorplan_gdf, index_single_example

    def generate_single_block(self, data_files, dataset_block):
        index_file = list()
        dataset = list()
        for i, _file in enumerate(data_files):
            try:
                if _file == "..\data\representation_prediction\00\92\5d23c62ac18f243dc740514b9d74\0001.txt":
                    print("NOK")
                floorplan_gdf, index_single_example = self.generate_single_example(_file)
                index_single_example["dataset_block"] = dataset_block
                index_file.append(index_single_example)
                dataset.append(floorplan_gdf)

            except Exception as e:
                log.error(f"Issue with file: {_file}: {e}")
                continue
        self.save_block(dataset_block=dataset_block, dataset=dataset)

        index_df = pd.concat(index_file)
        index_df = index_df.fillna(0)
        index_df.to_csv(
            self.output_directory / f"index_floorplans_{dataset_block}.csv", index=False
        )

    def run(self, dataset_size=1000, n_jobs=-1, starting_block=0):
        data_files = sorted(self.input_directory.glob("**/*.txt"))
        log.info(f"Creating shape file based on {len(data_files)} samples.")

        n_blocks = int(len(data_files) / dataset_size)
        data_file_blocks = split(data_files, n_blocks)
        dataset_blocks_ids = np.arange(len(data_file_blocks))

        if starting_block != 0:
            data_file_blocks = data_file_blocks[starting_block:]
            dataset_blocks_ids = dataset_blocks_ids[starting_block:]
            log.info(f"Starting at a different block number: {starting_block}.")
            n_blocks = int(len(data_file_blocks))

        log.info(f"Going through {n_blocks} blocks in parallel.")
        Parallel(n_jobs=n_jobs)(
            delayed(self.generate_single_block)(data_file_block, dataset_block_id)
            for (data_file_block, dataset_block_id) in tqdm(
                zip(data_file_blocks, dataset_blocks_ids)
            )
        )

        log.info("Combining the separate index files..")
        index_floorplan = sorted(self.output_directory.glob("index_floorplans_*.csv"))
        log.info(f"Found {len(index_floorplan)} index block files.")
        index_files = pd.concat([pd.read_csv(_file) for _file in index_floorplan])
        index_files = index_files.fillna(0)
        index_files.to_csv(self.output_directory / "index_floorplans.csv", index=False)
