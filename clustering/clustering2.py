import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from get_vulnerability_vector import get_vector_per_tool, tool_vectors
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Read the CSV file to populate tool_vectors (assuming you already have this logic)
df = pd.read_csv('../vulnerabilities_log.csv')
for index, row in df.iterrows():
    get_vector_per_tool(row)

# Define DBSCAN parameters
eps = 0.5  # Distance threshold
min_samples = 5  # Minimum number of samples in a cluster

# Initialize DBSCAN
dbscan = DBSCAN(eps=eps, min_samples=min_samples)

# Loop over each tool and cluster its vectors
for tool, vectors in tool_vectors.items():
    flattened_vectors = []

    # Flatten vulnerability scores for the current tool
    for items in vectors:
        for item in items:
            if int(item['lineno']) != -1:
                flattened_vectors.append(item['vulnerability'])

    # Convert to numpy array and reshape for compatibility with DBSCAN
    X = np.array(flattened_vectors).reshape(-1, 1)
    print(tool)
    if len(X)==0:
        continue
    # Standardize data
    X = StandardScaler().fit_transform(X)

    # Perform DBSCAN clustering
    clusters = dbscan.fit_predict(X)

    # Print the clusters for each tool (just for demonstration)
    print(f"Tool: {tool}")
    print(f"Clusters: {clusters}")

    # Optionally, you can visualize the clusters
    plt.figure(figsize=(8, 6))
    plt.scatter(range(len(flattened_vectors)), flattened_vectors, c=clusters, cmap='viridis')
    plt.title(f"DBSCAN Clustering Results for {tool}")
    plt.xlabel("Data Points")
    plt.ylabel("Vulnerability Score")
    plt.colorbar(label='Cluster Label')
    plt.show()
