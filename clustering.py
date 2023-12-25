import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import distance
import plotly.graph_objects as go



def clustering(data_file, eps, min_samples, z_threshold):
    # Read the LiDAR point cloud data into a pandas DataFrame
    df = pd.read_csv(data_file)
    
    # Thresholding: Remove points below the specified Z threshold
    df = df[df['Point:2'] >= z_threshold]
    
    # Select the columns of interest for DBSCAN
    data = df[['Point:0', 'Point:1', 'Point:2']]
    
    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(data)
    return data, labels