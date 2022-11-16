from tqdm import tqdm
import pandas as pd
from typing import Union
# from nltk.tokenize import word_tokenize

from dqfit.resource_helpers.r401 import ResourceHelper  # shoutout JL
from dqfit.model import DQIModel


def get_supported_resources(bundles: Union[pd.DataFrame, list]) -> pd.DataFrame:
    bundles = pd.DataFrame(bundles) if type(bundles) == list else bundles
    bundles = bundles.reset_index().rename(columns={"index":"bundle_index"})
    
    resources = pd.json_normalize(
        bundles["entry"].explode()
    )  # concise-ish but doesn't scale great
    resources.columns = [col.replace("resource.", "") for col in resources.columns]
    SUPPORTED_RESOURCES = DQIModel().SUPPORTED_RESOURCES
    supported_resources = resources[resources["resourceType"].isin(SUPPORTED_RESOURCES)]
    
    supported_resources = supported_resources.dropna(
        how="all", axis=1
    )  # drop extra columns
    supported_resources = supported_resources.reset_index(drop=True)
    return supported_resources


def _get_resource_features(resources: pd.DataFrame) -> pd.DataFrame:
    features = pd.DataFrame()
    feature_map = {
        "_ref": ResourceHelper.get_patient_reference,
        "bundle_index": ResourceHelper.get_bundle_index,
        "id": ResourceHelper.get_id,
        "resource_type": ResourceHelper.get_type,
        "date": ResourceHelper.get_date,
        "code": ResourceHelper.get_code,  # -> codes?
        "system": ResourceHelper.get_system,
        "val": ResourceHelper.get_val,
        "gender": ResourceHelper.get_patient_gender,
        "age_decile": ResourceHelper.get_patient_age_decile,
        # "zip5": ResourceHelper.get_patient_zip5,
    }
    for k, v in tqdm(feature_map.items()):
        features[k] = resources.apply(v, axis=1)

    # blank date for the 8888-12-01s of the world
    features["date"] = pd.to_datetime(features["date"], errors="coerce")
    date_index = pd.DataFrame(dict(date=pd.date_range(start="2016-01-01", end=pd.to_datetime("today"))))
    date_index = date_index.reset_index().rename(columns={"index":"date_index"})
    features = features.merge(date_index, how='left')
    return features


def transform(bundles: Union[pd.DataFrame, list], version="r401") -> pd.DataFrame:
    """
        Takes in Resources, applies ResourceHelper Logic.
        Versioning API WIP
    """
    resources = get_supported_resources(bundles)
    return _get_resource_features(resources)

    