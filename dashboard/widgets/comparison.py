import sys
import math
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import numpy as np

root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from library.config import set_data_root
from widgets.utilities import scenario, full_palette
from library.language import TEXTS

color_mapping = full_palette()

def _circles_chart(labels, values, cmap):

    # To match the area to the marker size, we need to take the square root of the value
    radii = [np.sqrt(v/math.pi) for v in values]
    height = 260

    radii = radii / max(radii) * 0.66 * height/2

    x_positions = [0,1,2] # TODO: Make this more robus at some point
    y_positions = [0, 0, 0]
    
    # Create the scatter plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_positions,  # Horizontal axis positions
        y=y_positions,  # Set y to 0 to align all circles horizontally
        mode='markers+text',
        marker=dict(
            size=radii*2,  # Set marker sizes corresponding to the radii
            color=[cmap[label] for label in labels],  # Different colors for each circle
            opacity=color_mapping['opacity'],
            sizemode='diameter',  # Ensure sizes are proportional to diameter
        ),
        text=labels,  # Labels for each circle
        textposition='bottom center',
        customdata=[f"{value:,.0f}" for value in values],
        hovertemplate=(
            "<b>%{text}</b><br><extra></extra>"
            "<b>Area</b>: %{customdata} ha.<br>"
        ),
    ))

    # Update layout to make sure the chart looks clean
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        height=height,
        margin=dict(l=0, r=40, t=10, b=10)
    )

    st.plotly_chart(fig, config={'displayModeBar': False})


def comparison_widget(geo, target_year, self_sufficiency, energy_scenario, h2, offwind, biogas_limit, modal):
    data_root = set_data_root()

    solar_path = data_root / scenario(geo, target_year, self_sufficiency, energy_scenario, h2, offwind, biogas_limit) / 'generators' / 'solar' / 'details.csv.gz'
    onwind_path = data_root / scenario(geo, target_year, self_sufficiency, energy_scenario, h2, offwind, biogas_limit) / 'generators' / 'onwind' / 'details.csv.gz'

    if solar_path.is_file():
        solar_details = pd.read_csv(solar_path, compression='gzip', index_col=0)
    if onwind_path.is_file():
        onwind_details = pd.read_csv(onwind_path, compression='gzip', index_col=0)

    area_per_turbine = 20

    total_land = 12_946_200
    solar_land = float(solar_details.loc['mod_units','solar'])
    onwind_land = float(onwind_details.loc['mod_units','onwind']) * area_per_turbine

    labels = ['Total land', 'solar', 'onwind']
    translated_labels = [TEXTS['Total land'], TEXTS['solar'], TEXTS['onwind']]
    values = [total_land, solar_land, onwind_land ]
    color_map = {TEXTS[label]: color_mapping[label] for label in labels}

    with st.container(border=False):
        _circles_chart(translated_labels, values, color_map)


