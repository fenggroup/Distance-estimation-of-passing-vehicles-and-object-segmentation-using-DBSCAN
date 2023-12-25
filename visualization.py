import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import distance
import plotly.graph_objects as go

def visualization(data, distance_threshold, labeled_objects, lidar_position, object_min_distance_points, output_df):
    # Create a 3D scatter plot
    fig = go.Figure()
    # Calculate the distance of all points to the LiDAR position
    all_points_distances = np.linalg.norm(data - lidar_position, axis=1)
    # Add a single trace for all points
    fig.add_trace(go.Scatter3d(
        x=data['Point:0'],
        y=data['Point:1'],
        z=data['Point:2'],
        mode='markers',
        marker=dict(
            colorscale='Plasma',  # Set a single color for all points
            size=2,  # Adjust the marker size as desired
            opacity=0.8,  # Adjust opacity to make the points less prominent
        ),
        customdata=all_points_distances,
        hovertemplate='Distance to LiDAR: %{customdata:.2f} m<br>' +
                      'X: %{x} m<br>' +
                      'Y: %{y} m<br>' +
                      'Z: %{z} m',
        name='All Points',  # Name this trace for legend
    ))
    # Find the point with the minimum distance to the LiDAR for red points
    red_object_ids = [object_id for object_id in np.unique(labeled_objects) if
                      object_id != 1]  # Assuming object ID 1 is not a car
    min_distance_red_car = None
    for object_id in red_object_ids:
        object_points = output_df[output_df['Object ID'] == object_id]
        if np.min(object_points['Distance']) <= distance_threshold and np.min(object_points['Distance']) > 0 and np.min(
                object_points['Point:1']) > 0:
            min_distance_red_car = np.min(object_points['Distance'])
            break  # Found the closest car, exit loop
    # Print the minimum distance of the identified car on the screen
    if min_distance_red_car is not None:
        print(f"Minimum Distance to the car on the left: {min_distance_red_car:.2f} m")
    else:
        print("No car found within the specified distance threshold and conditions.")
    # Iterate over unique object IDs and add scatter traces for objects
    for object_id in np.unique(labeled_objects):
        object_points = output_df[output_df['Object ID'] == object_id]

        # Get the point with the minimum distance to LiDAR for the current object
        min_distance_point = object_min_distance_points[object_id - 1]

        if object_id == 1:
            color = 'orange'  # Color for objects with object ID 1 (assuming not a car, it's the lidar)
        else:
            # Check if the minimum distance is within the specified distance threshold and greater than 0
            if np.min(object_points['Distance']) <= distance_threshold and np.min(
                    object_points['Distance']) > 0 and np.min(object_points['Point:1']) > 0:
                color = 'red'  # Color for objects within the specified distance threshold and greater than 0
            else:
                color = 'blue'  # Color for objects outside the specified distance threshold or less than or equal to 0

        fig.add_trace(go.Scatter3d(
            x=object_points['Point:0'],
            y=object_points['Point:1'],
            z=object_points['Point:2'],
            mode='markers',
            marker=dict(
                color=color,
                size=3,  # Set a larger marker size for the point with minimum distance
                opacity=0.8,
            ),
            customdata=object_points['Distance'],
            hovertemplate='Distance to LiDAR: %{customdata:.2f} m<br>' +
                          'X: %{x} m<br>' +
                          'Y: %{y} m<br>' +
                          'Z: %{z} m',
            name=f'Object {object_id}',
        ))

        # Add an additional trace for the point with minimum distance to LiDAR
        fig.add_trace(go.Scatter3d(
            x=[min_distance_point[0]],
            y=[min_distance_point[1]],
            z=[min_distance_point[2]],
            mode='markers',
            marker=dict(
                color='green',
                size=8,  # Set an even larger marker size for the point with minimum distance
                opacity=1.0,
            ),
            customdata=[np.min(object_points['Distance'])],
            hovertemplate='Distance to LiDAR: %{customdata:.2f} m<br>' +
                          'X: %{x} m<br>' +
                          'Y: %{y} m<br>' +
                          'Z: %{z} m',
            name=f'Object {object_id} - Min Distance Point',
        ))
    # Customize layout and axis labels
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='manual',  # Set aspect ratio manually
            aspectratio=dict(x=5, y=1, z=0.7),  # Set the desired aspect ratio for X, Y, and Z axes
        ),
        width=1200,  # Specify the width of the figure in pixels
        height=800,  # Specify the height of the figure in pixels
    )
    # Show the 3D plot
    fig.show()


