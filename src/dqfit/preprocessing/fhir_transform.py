import pandas as pd
from dqfit.preprocessing.adapters.r401 import get_fhir_features
from tqdm import tqdm


def transform_bundles(bundles: pd.DataFrame) -> pd.DataFrame:
    entries = bundles[["bundle_index", "entry"]].explode("entry")
    resources = [e["resource"] for e in entries['entry']]
    features = []
    for r in tqdm(resources):
        # could parralelize this 
        features.append(get_fhir_features(r))
    features = pd.DataFrame(features)
    features.insert(0, 'bundle_index', list(entries['bundle_index']))
    return features
