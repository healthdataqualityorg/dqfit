import pandas as pd
import dqfit

def cohort_bundles_test(request):
    request_json = request.get_json()
    bundles = request_json['bundles']
    bundles = pd.DataFrame(bundles)
    scored_bundles = dqfit.fit_transform(bundles)
    resp = {
        "patient_level_score": list(scored_bundles['score']),
        "dqi": scored_bundles['score'].median()
    }
    return resp

