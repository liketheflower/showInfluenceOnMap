from typing import List, Tuple

import folium
import numpy as np
import pandas as pd

colors = ["#66bd63", "#fdae61"]


def vis_on_map(
    countries: List[Tuple[float, float]],
    num_researchers_cite_my_work: List[int] = None,
    num_institutions_cite_my_work: List[int] = None,
    delta_for_latitude_for_better_vis: float = 1.0,
    save_fn="index.html",
    opacity_val=1.0,
):
    world_map = folium.Map(tiles="cartodbpositron")
    N = len(countries)
    if num_institutions_cite_my_work is None:
        num_institutions_cite_my_work = [None] * N
    if num_researchers_cite_my_work is None:
        num_researchers_cite_my_work = [None] * N
    for (lat, long), num_researcher, num_inst in zip(
        countries, num_researchers_cite_my_work, num_institutions_cite_my_work
    ):
        if num_researcher is not None:
            folium.CircleMarker(
                location=[lat, long],
                radius=int(num_researcher),
                color=colors[0],
                opacity=opacity_val,
                fill_color=colors[0],
                fill_opacity=opacity_val,
                fill=True,
            ).add_to(world_map)
        if num_inst is not None:
            folium.RegularPolygonMarker(
                location=[lat - delta_for_latitude_for_better_vis, long],
                radius=int(num_inst),
                color=colors[1],
                opacity=opacity_val,
                fill_color=colors[1],
                fill_opacity=opacity_val,
                number_of_sides=6,
                fill=True,
            ).add_to(world_map)
    world_map.save(save_fn)


if __name__ == "__main__":
    # Test based on using USA as a sample
    countries = [(37.6, -95.665)]
    num_researchers_cite_my_work = [10]
    num_institutions_cite_my_work = [20]
    vis_on_map(
        countries,
        num_researchers_cite_my_work=num_researchers_cite_my_work,
        num_institutions_cite_my_work=num_institutions_cite_my_work,
    )
