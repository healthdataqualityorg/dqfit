from typing import Union
import json
from zipfile import ZipFile

import pandas as pd


class BundleQuery:

    """Returns n x m DataFrame where n is count of FHIR Bundles in Cohort"""

    @staticmethod
    def zipfile_query(cohort_zip_path: str) -> pd.DataFrame:
        zf = ZipFile(cohort_zip_path)
        bundles = [json.load(zf.open(f)) for f in zf.namelist()[1::]]
        return pd.DataFrame(bundles)

    @staticmethod
    def directory_query(cohort_dir: str) -> pd.DataFrame:
        ...

    @staticmethod
    def big_query() -> pd.DataFrame:
        ...


class CohortQuery:

    """Returns n x m DataFrame where n is count of FHIR Bundles in Cohort"""

    # def __init__(self, cohort_zip_path: str) -> None:
    #     .
        
    
    
    def _load_zipfile(cohort_zip_path: str) -> pd.DataFrame:
        zf = ZipFile(cohort_zip_path)
        bundles = [json.load(zf.open(f)) for f in zf.namelist()[1::]]
        return pd.DataFrame(bundles)

    # @staticmethod
    # def directory_query(cohort_dir: str) -> pd.DataFrame:
    #     ...

    # @staticmethod
    # def big_query() -> pd.DataFrame:
    #     ...


def get_supported_resources(bundles: Union[pd.DataFrame, list]) -> pd.DataFrame:
    if type(bundles) == list:
        bundles = pd.DataFrame(bundles)
    # MedicationDispense ? check to see where CQL examples sit with this
    SUPPORTED_RESOURCES = [
        "Patient",
        "Procedure",
        "Condition",
        "Observation",
        "Immunization",
        # "AllergyIntolerance", getting erros on synthrea
    ]
    resources = pd.json_normalize(
        bundles["entry"].explode()
    )  # concise-ish but doesn't scale great
    resources.columns = [col.replace("resource.", "") for col in resources.columns]
    supported_resources = resources[resources["resourceType"].isin(SUPPORTED_RESOURCES)]
    supported_resources = supported_resources.dropna(how="all", axis=1) # drop extra columns
    supported_resources = supported_resources.reset_index(drop=True)
    return supported_resources



def get_resource_features(resources: pd.DataFrame) -> pd.DataFrame:
    """
        Takes in Resources, applies ResourceHelper Logic (which is where we can version)
    """
    features = pd.DataFrame()
    feature_map = {
        "_ref": ResourceHelper.get_patient_reference,
        "id": ResourceHelper.get_id,
        "resource_type": ResourceHelper.get_type,
        "date": ResourceHelper.get_date,
        "code": ResourceHelper.get_code, # -> codes?
        "system": ResourceHelper.get_system,
        "val": ResourceHelper.get_val,
        "gender": ResourceHelper.get_patient_gender,
        "age_decile": ResourceHelper.get_patient_age_decile,
        # "zip5": ResourceHelper.get_patient_zip5,
    }
    for k, v in feature_map.items():
        features[k] = resources.apply(v, axis=1) 

    features['date'] = pd.to_datetime(features['date'])    
    return features

resources = get_supported_resources(bundles)
resource_features = get_resource_features(resources)
resource_features