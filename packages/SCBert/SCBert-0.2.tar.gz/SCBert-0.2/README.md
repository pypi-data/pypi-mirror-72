# Sentence Clustering with BERT (SCB)

Sentence Clustering with BERT project which aim to use state-of-the-art BERT models to compute vectors for sentences. A few tools are also implemented to explore those vectors and how sentences are related to each others in the latent space. 

### Demonstration 

- **Create vectors from raw data :**

```
#How to transform raw french texts into vectors using BERT model. 
from SCBert.SCBert import Vectorizer

vectorizer = Vectorizer("flaubert")
text_vectors = vectorizer.vectorize(data)
```

- **Explore the embedded space :**
```
#How to explore the relation in your data. 
from SCBert.SCBert import EmbeddingExplorer

ee = EmbeddingExplorer(data,text_vectors)
labels = ee.cluster(k=3)                     #Cluster with k-means 
ee.extract_keywords()                        #Extract keywords using Rake algorithm, then accessible with ee.keywords
ee.explore(color = labels)                   #Generate a plot with PCA of the embedded vectors with colors corresponding to the labels 
```

### Built-in example

There is a built-in example that you can find in the example folder. It comes with it's own data which is the CLS-fr composed of Amazon reviews from different sources (DVD, CD, Livres)

### Installation 

You can either download the zip file or use the Pypi package that you can install with the following command : 

```
> pip install SCBert
```


If you encounter problems during the installation it may be because of the multi-rake dependy with cld2-cffi. I will try to address this later on. To bypass, just follow the instructions : 

```
> export CFLAGS="-Wno-narrowing"
> pip install cld2-cffi
> pip install multi-rake
```
