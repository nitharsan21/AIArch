import logging

import pandas as pd

from mlgan.core import labeling
from mlgan.dataset_builder import ImageBaseGenerator

log = logging.getLogger(__name__)


class ImageFloorplanGenerator(ImageBaseGenerator):


    def create_input_gdf(self, areas_gdf):

        areas_gdf = areas_gdf.copy()
        areas_gdf["colors"] = "black"
        return areas_gdf

    def create_output_gdf(self, areas_gdf):

        areas_gdf = areas_gdf.copy()
        CATEGORIES_TO_DROP = ["wall", "door", "entrance"]
        areas_gdf = areas_gdf.loc[
            ~areas_gdf["category"].isin(CATEGORIES_TO_DROP)
        ].copy()
        colormap = labeling.get_room_color_map()
        colors = pd.DataFrame(
            list(
                areas_gdf["category"]
                .apply(lambda cat: [x / 255 for x in colormap[cat]])
                .values
            ),
            columns=["color_r", "color_g", "color_b"],
        )
        areas_gdf["colors"] = list(colors[["color_r", "color_g", "color_b"]].values)

        areas_gdf = areas_gdf.sort_values("area_size", ascending=False)
        return areas_gdf
