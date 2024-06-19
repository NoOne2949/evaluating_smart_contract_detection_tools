import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Example data: a list of vectors (numpy array)
data = np.array([
    [1.0, 2.0],
    [1.5, 1.8],
    [5.0, 8.0],
    [8.0, 8.0],
    [1.0, 0.6],
    [9.0, 11.0],
    [8.0, 2.0],
    [10.0, 2.0],
    [9.0, 3.0]
])

# Determine the optimal number of clusters using the elbow method
sse = []
k_range = range(1, 10)
for k in k_range:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(data)
    sse.append(kmeans.inertia_)

# Plotting the elbow graph
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(k_range, sse, 'bx-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Sum of squared distances (SSE)')
plt.title('Elbow Method for Optimal Number of Clusters')

# Define the number of clusters (e.g., 3)
num_clusters = 3

# Create an instance of the K-means algorithm
kmeans = KMeans(n_clusters=num_clusters)

# Fit the algorithm to the data
kmeans.fit(data)

# Get the cluster centroids
centroids = kmeans.cluster_centers_

# Get the cluster labels for each data point
labels = kmeans.labels_

# Print the results
print("Cluster centroids:")
print(centroids)

print("\nCluster labels for each data point:")
print(labels)

# Visualize the clusters
colors = ['r', 'g', 'b']
for i in range(num_clusters):
    points = data[labels == i]
    plt.scatter(points[:, 0], points[:, 1], s=100, c=colors[i], label=f'Cluster {i+1}')

# Visualize the centroids
plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='yellow', marker='X', label='Centroids')

plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('K-means Clustering')
plt.show()
