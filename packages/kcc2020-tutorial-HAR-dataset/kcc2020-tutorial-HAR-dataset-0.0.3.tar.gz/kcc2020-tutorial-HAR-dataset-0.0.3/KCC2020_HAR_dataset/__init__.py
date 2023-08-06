import pandas as pd
import pickle
import gzip
from typing import Dict, List
import os

with gzip.open(os.path.join(os.path.dirname(__file__), 'res', 'HAPT.pkl.gz'), 'rb') as f:
    __dfs = pickle.load(f)

__remove_no_labels: pd.DataFrame = lambda remove_no_lavels, df: df if not remove_no_lavels else df[df.label != -1]


def load_by_user(uid: int, remove_no_lavels=True) -> pd.DataFrame:
    if uid <= 30:
        return None
    return __remove_no_labels(remove_no_lavels, __dfs[uid].copy())


def load_all(remove_no_lavels=True) -> Dict[int, List[pd.DataFrame]]:
    result = dict()
    for uid in __dfs:
        for df in __dfs[uid]:
            result.setdefault(uid, list()).append(__remove_no_labels(df.copy(), remove_no_lavels))
    return result
