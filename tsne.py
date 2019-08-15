#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_mldata
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# import the main drawing library
from matplotlib.widgets import Button
from matplotlib.text import Annotation



# In[3]:



df = pd.read_csv('dataset.csv')
num_instances = len(df.index)

feat_cols = df.columns[:-1]
print(feat_cols)

print('Size of the dataframe: {}'.format(df.shape))

# In[4]:

# # For reproducability of the results
# np.random.seed(42)
# rndperm = np.random.permutation(df.shape[0])
n_components = 100
pca = PCA(n_components=n_components)
pca_result = pca.fit_transform(df[feat_cols].values)

# df['pca-one'] = pca_result[:,0]
# df['pca-two'] = pca_result[:,1] 
# df['pca-three'] = pca_result[:,2]
print('Explained variation per principal component: {}'.format(np.sum(pca.explained_variance_ratio_)))
print(pca_result)
# In[]:
new_cols = ['x{}'.format(i) for i in range(n_components)]
new_df = pd.DataFrame(data=pca_result, columns=new_cols)
new_df['class_val'] = df['class_val']

print(new_df['class_val'])

# In[]
print(df['class_val'])
# In[]
fig = plt.figure(figsize=(16,10))
method_name_count = df['method_name'].nunique()
ax = None

def draw_scatterplot():
    global ax

    ax = sns.scatterplot(
        x="pca-one", y="pca-two",
        hue="method_name",
        palette=sns.color_palette("hls", method_name_count),
        data=df,
        legend="full",
        alpha=0.8,
        s=1000,
        picker=1
    )

    # ax.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
    ax.legend(ncol=1, loc='center left', bbox_to_anchor=(-0.15, 0.5))

draw_scatterplot()

# create and add an annotation object (a text label)
def annotate(axis, text, x, y):
    text_annotation = Annotation(text, xy=(x, y), xycoords='data', backgroundcolor="w")
    axis.add_artist(text_annotation)

def onpick(event):
        # step 1: take the index of the dot which was picked
    ind = event.ind

    # step 2: save the actual coordinates of the click, so we can position the text label properly
    label_pos_x = event.mouseevent.xdata
    label_pos_y = event.mouseevent.ydata

    # just in case two dots are very close, this offset will help the labels not appear one on top of each other
    offset = 0

    # if the dots are to close one to another, a list of dots clicked is returned by the matplotlib library
    for i in ind:
        # step 3: take the label for the corresponding instance of the data
        label = generated_labels[i]

        # step 4: log it for debugging purposes
        print("index", i, label)

        # step 5: create and add the text annotation to the scatterplot
        annotate(
            ax,
            label,
            label_pos_x + offset,
            label_pos_y + offset
        )

        # step 6: force re-draw
        ax.figure.canvas.draw_idle()

        # alter the offset just in case there are more than one dots affected by the click
        offset += 0.5

ax.figure.canvas.mpl_connect("pick_event", onpick)

plt.plot()

plt.show()

# N = 10000
# df_subset = df.loc[rndperm[:N],:].copy()
# data_subset = df_subset[feat_cols].values
# pca = PCA(n_components=3)
# pca_result = pca.fit_transform(data_subset)
# df_subset['pca-one'] = pca_result[:,0]
# df_subset['pca-two'] = pca_result[:,1] 
# df_subset['pca-three'] = pca_result[:,2]
# print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))


# In[11]:

import time


time_start = time.time()
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(df[feat_cols].values)
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))


# In[14]:


df['tsne-2d-one'] = tsne_results[:,0]
df['tsne-2d-two'] = tsne_results[:,1]
plt.figure(figsize=(16,10))
sns.scatterplot(
    x="tsne-2d-one", y="tsne-2d-two",
    hue="method_name",
    palette=sns.color_palette("hls", method_name_count),
    data=df,
    legend="full",
    alpha=0.8,
    s=1000
)


# In[ ]:

pca_50 = PCA(n_components=50)
pca_result_50 = pca_50.fit_transform(df[feat_cols].values)

print('Cumulative explained variation for 50 principal components: {}'.format(np.sum(pca_50.explained_variance_ratio_)))

# In[ ]:

time_start = time.time()
tsne = TSNE(n_components=2, verbose=0, perplexity=40, n_iter=300)
tsne_pca_results = tsne.fit_transform(pca_result_50)
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))

df['tsne-pca50-one'] = tsne_pca_results[:,0]
df['tsne-pca50-two'] = tsne_pca_results[:,1]

plt.figure(figsize=(16,10))
sns.scatterplot(
    x="tsne-pca50-one", y="tsne-pca50-two",
    hue="method_name",
    palette=sns.color_palette("hls", method_name_count),
    data=df,
    legend="full",
    alpha=0.8,
    s=1000
)