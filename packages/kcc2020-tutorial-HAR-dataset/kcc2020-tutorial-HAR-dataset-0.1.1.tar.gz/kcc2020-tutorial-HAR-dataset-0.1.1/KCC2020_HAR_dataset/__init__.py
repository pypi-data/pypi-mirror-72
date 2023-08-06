import pandas as pd
import pickle
import gzip
from typing import Dict, List
import os

with gzip.open(os.path.join(os.path.dirname(__file__), 'res', 'HAPT.pkl.gz'), 'rb') as f:
    __dfs = pickle.load(f)


def __get_filtered_copy(df: pd.DataFrame, include_transitions: bool, remove_no_labels: bool) -> List[pd.DataFrame]:
    result = df.copy()
    result = result[result.label != -1] if  remove_no_labels else result
    result = result if include_transitions else result[result.label <= 6]
    return result


def load_by_user(uid: int, include_transitions=False, remove_no_labels=True) -> List[pd.DataFrame]:
    if uid > 30:
        return None
    result = list()
    for df in __dfs[uid]:
        result.append(__get_filtered_copy(df, include_transitions, remove_no_labels))
    return result


def load_all(include_transitions=False, remove_no_labels=True) -> Dict[int, List[pd.DataFrame]]:
    result = dict()
    for uid in __dfs:
        for df in __dfs[uid]:
            result.setdefault(uid, list()).append(__get_filtered_copy(df, include_transitions, remove_no_labels))
    return result
