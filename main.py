import pandas as pd
import numpy as np
import plotly.graph_objects as go
from car_identification import identify_car


# Provide the path to your LiDAR point cloud data file
data_file_path = 'data/BlackTruck2_frame14059 (Frame 14059).csv'

# Set the DBSCAN parameters
eps = 0.6  # DBSCAN epsilon parameter
min_samples = 250  # DBSCAN minimum number of samples parameter

# Provide the path for the output file to save the labeled objects and distances
output_file_path = 'outputs/output_frame14059 (Frame 14059).csv'

# Set the Z threshold to exclude points below this value
z_threshold = -0.7  # Adjust this threshold as per the requirements

# Set the distance threshold for identifying the car
distance_threshold = 3.0  # 3 meters 


# Call the function to perform segmentation, distance calculation, and identify the car within the specified threshold
identify_car(data_file_path, eps, min_samples, distance_threshold, z_threshold, output_file_path)