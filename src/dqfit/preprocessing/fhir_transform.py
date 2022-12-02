import pandas as pd
from dqfit.preprocessing.adapters.r401 import get_fhir_features


def transform_bundles(bundles: pd.DataFrame) -> pd.DataFrame:
    entries = bundles[["bundle_index", "entry"]].explode("entry")
    resources = [e["resource"] for e in entries['entry']] 
    features = pd.DataFrame([get_fhir_features(r) for r in resources])
    features.insert(0, 'bundle_index', list(entries['bundle_index']))
    return features
