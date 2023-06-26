import logging

import geopandas as gpd
import pandas as pd

from mlgan.core import preprocessing
from mlgan.dataset_builder import ImageBaseGenerator

log = logging.getLogger(__name__)


class ImageStructureGenerator(ImageBaseGenerator):


    def find_overlap(self, gdf1, gdf2):
        gdf1.crs = "epsg:4326"
        gdf2.crs = "epsg:4326"
        return gpd.sjoin(gdf1, gdf2).drop("index_right", axis=1)

    def create_input_gdf(self, relevant_floorplan_gdf):

        AREA_SIZE_DIVIDER = 25000
        MIN_BUFFER_SIZE = 3
        MAX_BUFFER_SIZE = 10
        wall_gdf = relevant_floorplan_gdf.loc[
            relevant_floorplan_gdf["category"] == "wall"
        ].copy()

        area = wall_gdf.unary_union.buffer(0.01).convex_hull.area

        buffer_size = area / AREA_SIZE_DIVIDER
        buffer_size = max(buffer_size, MIN_BUFFER_SIZE)
        buffer_size = min(buffer_size, MAX_BUFFER_SIZE)
        wall_gdf.geometry = wall_gdf.buffer(buffer_size, join_style=2, cap_style=3)

        return wall_gdf

    def create_output_gdf(self, relevant_floorplan_gdf):

        # wall buffer size
        AREA_SIZE_DIVIDER = 25000
        MIN_BUFFER_SIZE = 3
        MAX_BUFFER_SIZE = 10
        wall_gdf = relevant_floorplan_gdf.loc[
            relevant_floorplan_gdf["category"] == "wall"
        ].copy()

        area = wall_gdf.unary_union.buffer(0.01).convex_hull.area

        buffer_size = area / AREA_SIZE_DIVIDER
        buffer_size = max(buffer_size, MIN_BUFFER_SIZE)
        buffer_size = min(buffer_size, MAX_BUFFER_SIZE)

        extended_doors = relevant_floorplan_gdf.loc[
            relevant_floorplan_gdf["category"] == "door"
        ].copy()
        extended_doors.geometry = extended_doors.buffer(buffer_size * 2, cap_style=2)
        extended_doors["colors"] = "blue"

        # Create outer walls
        outer_walls = preprocessing.create_outer_bounderies(
            relevant_floorplan_gdf.loc[
                relevant_floorplan_gdf["category"] != "balcony"
            ].copy(),
            buffer=0.1,
        )

        entrance = relevant_floorplan_gdf.loc[
            relevant_floorplan_gdf["category"] == "entrance"
        ].copy()

        walls = self.create_input_gdf(relevant_floorplan_gdf)
        walls["colors"] = "black"

        windows = self.find_overlap(extended_doors, outer_walls)
        windows["colors"] = "red"

        if not entrance.empty:
            entrance_gdf = self.find_overlap(windows, entrance)
            entrance_gdf["colors"] = "green"
            return pd.concat([walls, extended_doors, windows, entrance_gdf])
        return pd.concat([walls, extended_doors, windows])
