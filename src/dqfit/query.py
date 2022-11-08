import json
from zipfile import ZipFile
import pandas as pd

class BundleQuery:

    """ Returns n x m DataFrame where n is count of FHIR Bundles in Cohort """

    @staticmethod
    def zipfile_query(cohort_zip_path: str) -> pd.DataFrame:
        zf = ZipFile(cohort_zip_path)
        filenames = zf.namelist()[1::]
        bundles = [json.load(zf.open(f)) for f in filenames]
        return pd.DataFrame(bundles)
    
    @staticmethod
    def directory_query(cohort_dir: str) -> pd.DataFrame:
        ...

    @staticmethod
    def big_query() -> pd.DataFrame:
        ...