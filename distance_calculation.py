import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import distance
import plotly.graph_objects as go

#   """
#   Calculates the distance between the LiDAR and each point in the object.

#   Args:
#     lidar_position: A NumPy array representing the LiDAR position.
#     object_points: A NumPy array of points belonging to a single object.

#   """


def calculate_distance(data, labels, output_file):
    # Calculate the distance between the LiDAR and each segmented object
    lidar_position = np.array([0, 0, 0])  # Assuming the LiDAR position as the origin (0, 0, 0)
    distances = []
    labeled_objects = []
    label_counter = 1
    object_coordinates = []
    object_min_distance_points = []  # Store the point with minimum distance to LiDAR for each object
    
    # Iterate through unique labels (clusters) in the data
    for label in np.unique(labels):
        if label == -1:
            continue  # Skip noise points (with labels -1)
        cluster_points = data[labels == label].values  # Extract points belonging to the current cluster
        cluster_distances = distance.cdist(cluster_points, [lidar_position]).flatten()
        min_distance_index = np.argmin(cluster_distances) # Find index of the minimum distance
        distances.extend(cluster_distances)
        labeled_objects.extend([label_counter] * len(cluster_points))
        label_counter += 1
        object_coordinates.extend(cluster_points)
        object_min_distance_points.append(cluster_points[min_distance_index])
    # Save the distances, labeled objects, and object coordinates to a new CSV file
    output_df = pd.DataFrame({'Object ID': labeled_objects, 'Distance': distances})
    output_df['Point:0'], output_df['Point:1'], output_df['Point:2'] = zip(*object_coordinates)
    output_df.to_csv(output_file, index=False)
    return labeled_objects, lidar_position, object_min_distance_points, output_df

