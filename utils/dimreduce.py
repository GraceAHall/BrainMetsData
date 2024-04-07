
import pandas as pd
import numpy as np
import umap
from sklearn.decomposition import PCA


def embedding_to_df(embedding: np.ndarray, samples: np.ndarray, meta: dict[str, dict]) -> pd.DataFrame:
    donors = [s.split('_')[0] for s in samples]
    primaries = [meta['primary'][d] for d in donors]
    commons = [meta['common'][d] for d in donors]
    genders = [meta['gender'][d] for d in donors]
    batches = [meta['batch'][d] for d in donors]

    embedding_df = pd.DataFrame(embedding, columns=('x', 'y'))
    embedding_df["ident"] = pd.Series(samples, dtype=str)
    embedding_df["primary"] = pd.Series(primaries, dtype=str)
    embedding_df["common"] = pd.Series(commons, dtype=str)
    embedding_df["gender"] = pd.Series(genders, dtype=str)
    embedding_df["batch"] = pd.Series(batches, dtype=str)
    return embedding_df

def run_pca(genes_df: pd.DataFrame) -> np.ndarray:
    genes_np = genes_df.to_numpy()
    reducer = PCA(n_components=2)
    embedding = reducer.fit_transform(genes_np)
    assert genes_df.shape[0] == embedding.shape[0]
    return embedding

def run_umap(genes_df: pd.DataFrame) -> np.ndarray:
    genes_np = genes_df.to_numpy()
    reducer = umap.UMAP(
        random_state=42,
        n_neighbors=3,
        min_dist=0.01,
    )
    embedding = reducer.fit_transform(genes_np)
    assert genes_df.shape[0] == embedding.shape[0]
    return embedding
