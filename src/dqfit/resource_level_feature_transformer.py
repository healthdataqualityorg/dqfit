import pandas as pd
# import swifter

from dqfit.resource_helpers.r401 import ResourceHelper

class ResourceLevelFeatureTransformer:

    def __init__(self, bundles: pd.DataFrame) -> None:
        self.bundles = bundles
        self.resources = self._get_resources()
        self.results = self._get_resource_features()

    def _get_resources(self) -> pd.DataFrame:
        resources = pd.json_normalize(self.bundles['entry'].explode()) 
        resources.columns = [col.replace("resource.","") for col in resources.columns]
        return resources

    def _get_resource_features(self, unique = False) -> pd.DataFrame:
        resources = self.resources
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
            # parrallel apply opportunity
            # features[k] = resources.swifter.apply(v, axis=1) # this was slower
            features[k] = resources.apply(v, axis=1) # this was slower

        return features