
import pandas as pd
import numpy as np
import umap
from sklearn.decomposition import PCA


def run_pca(genes_df: pd.DataFrame) -> pd.DataFrame:
    genes_np = genes_df.to_numpy()
    reducer = PCA(n_components=2)
    embedding = reducer.fit_transform(genes_np)
    return pd.DataFrame(embedding, index=genes_df.index.values, columns=('x', 'y'))

def run_umap(genes_df: pd.DataFrame) -> pd.DataFrame:
    genes_np = genes_df.to_numpy()
    reducer = umap.UMAP(
        random_state=42,
        n_neighbors=3,
        min_dist=0.01,
    )
    embedding = reducer.fit_transform(genes_np)
    return pd.DataFrame(embedding, index=genes_df.index.values, columns=('x', 'y'))
