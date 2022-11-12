import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from dqfit.visualize import draw_score_distribution

# from typing import Optional, List


def fit_transform(bundles: pd.DataFrame) -> pd.DataFrame:
    """Extends sklearn syntax"""
    if type(bundles) == list:
        bundles = pd.DataFrame(bundles)
    bundles["y"] = bundles["entry"].apply(lambda x: len(x))
    bundles[["y"]] = MinMaxScaler().fit_transform(bundles[["y"]])
    bundles["score"] = bundles["y"].apply(lambda x: int(x * 100))
    bundles["group"] = bundles["score"].apply(lambda x: "pass" if x > 7 else "fail")
    return bundles


def visualize(scored_bundles: pd.DataFrame) -> None:
    draw_score_distribution(scored_bundles)
