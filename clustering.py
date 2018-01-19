from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

dataset = pd.read_csv('clusteringData.csv')
#print(dataset)

KM = KMeans(n_clusters=4, init='k-means++', random_state=170)

KM = KM.fit(dataset)

print("The cluster centroids are: \n", KM.cluster_centers_)
print("Cluster", KM.labels_)
print("Sum of distances of samples to their closest cluster center: ", KM.inertia_)

#colors = ['blue','yellow']
#plt.scatter(dataset.Subjectivity, dataset.numVerified, c=KM.labels_, cmap=matplotlib.colors.ListedColormap(colors), s=75)
#plt.show()

#colors = ['blue','red']
#plt.scatter(dataset.Subjectivity, dataset.Time, c=KM.labels_, cmap=matplotlib.colors.ListedColormap(colors), s=75)
#plt.show()

#dataset.Subjectivity, dataset.Polarity, dataset.Time, dataset.numTweets, dataset.sumRetweets, dataset.sumFaves, dataset.sumFollowers, dataset.numVerified


fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
ax.scatter(dataset.Subjectivity, dataset.numVerified, dataset.numTweets, c=KM.labels_, s=75)
plt.show()
