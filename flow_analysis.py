# Program to analyse the average flow rate of streams in England and Wales
# Data taken from NRFA (National River Flow Archive) website: https://nrfa.ceh.ac.uk/data/flow/england-and-wales
# Date: 08/11/2022
# Author: Fawaz Zaman
# Team 3 CBIM2

# Required modules (use !pip install <module>, if not installed)):
import pandas as pd
import plotly as py
import plotly.express as px # For map visualisation
import plotly.graph_objects as go # For map visualisation
import io

# Modules unused for now
# import numpy as np 
# import matplotlib.pyplot as plt

# Definition of a 'stream' for project purposes
#    1 m3/s = 1,000 L/s
upper_flow_rate = 1.2; # m3/s
lower_flow_rate = 0.5; # m3/s

# Read in the data
df = pd.read_csv(r"C:\Users\fawaz\OneDrive - Durham University\Team 3 Water Wheel\General\River Flow Data\nrfa-station-metadata-2022-11-08.csv")
quartile_col = 'gdf-q70-flow' # Look at the xth percentile flow rate [HAS TO BE A CSV COLUMN]

streams = df[(df[quartile_col] < upper_flow_rate) & (df[quartile_col] > lower_flow_rate)]; # Dataset of streams with flow rates between the upper and lower limits
print(streams[quartile_col].describe()) # Summary statistics of the streams' flow rates

# Plot the map
fig = px.scatter_geo(streams, lat = 'latitude', lon='longitude', color = quartile_col, color_continuous_scale=px.colors.sequential.Inferno, fitbounds="locations", hover_name='name')
fig.update_layout(title = 'Average flow rate of streams in England and Wales', geo=dict(
        center=dict(
            lat=54.06835,
            lon=-2.86108,
        ))) # Center the map on UK
py.offline.plot(fig, filename='river_map_interactive.html') # Save the map as an interactive HTML file


# Write stream data to a CSV file
streams.to_csv('streams.csv', index=False)

# Write summary statistics to a txt file
with open('summary_statistics.txt', 'w') as f:
    f.write('Summary statistics of the streams\' flow rates, in m3/s: \n')
    f.write(f'With an upper flow rate of {upper_flow_rate} m3/s and a lower flow rate of {lower_flow_rate} m3/s, there are {len(streams)} streams in England and Wales, suitable for analysis. \n')
    f.write(streams[quartile_col].describe().to_string())