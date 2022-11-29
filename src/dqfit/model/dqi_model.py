
import plotly.express as px
import pandas as pd

from dqfit.preprocessing import ResourceFeatures
from dqfit.query import weights_query


class DQIModel:
    def __init__(self, context: list =["BCSE","COLE"]) -> None:
        self.context = context

    @staticmethod
    def set_pass_fail(X, threshold=2):
        if X >= threshold:
            return "pass"
        else:
            return "fail"

    def patient_level_score(self, bundles):
        RF = ResourceFeatures.transform(bundles)
        
        def _get_patient_features(resource_level_features):
            # tidy this up
            df = resource_level_features.copy()
            df = df[df["resource_type"] == "Patient"].dropna(how="all", axis=1)
            # display(PF)
            df["dim_type"] = "resource_type"
            df["dim_key"] = "Patient"
            df["dim_weight"] = 1
            return df

        dim_weights = weights_query(context = self.context)
        contexts = []
        for context in dim_weights["context"].unique():
            context_dim_weights = dim_weights[dim_weights["context"] == context]
            weighted_resource_features = RF.copy()
            WPF = _get_patient_features(RF)
            WRF = weighted_resource_features.merge(
                context_dim_weights, left_on="code", right_on="dim_key"
            )
            C = pd.concat([WPF, WRF])  # gross fix this
            C["context"] = context  # todo set WPF on a per context level
            contexts.append(C)

        W = pd.concat(contexts)
        D = (
            W.groupby(["bundle_index", "context", "dim_key"])
            .agg(dim_score=("dim_weight", "sum"))
            .reset_index()
        )
        fitness_scores = (
            D.groupby(["context", "bundle_index"])
            .agg(patient_level_score=("dim_score", "sum"))
            .reset_index()
        )
        fitness_scores["outcome"] = fitness_scores["patient_level_score"].apply(
            self.set_pass_fail
        )
        return fitness_scores

    @staticmethod
    def visualize(scores):
        
        print(scores['outcome'].value_counts(normalize=True))
        cohort_outcomes = (
            scores.groupby(["context", "outcome"])
            .agg(count=("outcome", "count"))
            .reset_index()
        )
        
        px.bar(
            cohort_outcomes.sort_values(["context","outcome"], ascending=False),
            x="context",
            y="count",
            color="outcome",
            title=f"Cohort Outcomes",
        ).show(renderer='notebook')

    # def cohort_level_scores(self):
    #     fitness_scores
    #     cohort_outcomes = fitness_scores.groupby(['context','outcome']).agg(count=("outcome","count")).reset_index()
    #     cohort_outcomes

# from typing import Union

# import pandas as pd
# import plotly.express as px
# from sklearn.preprocessing import MinMaxScaler, StandardScaler
# from pathlib import Path

# # could be an abstraction
# class DQIModel:



#     def __init__(self, context="systolic") -> None:
#         """Does stuff"""
#         self.context = context

#     @property
#     def weights(self):
#         package_dir = Path(__file__).parent
#         dimension_weights = pd.read_csv(
#             f"{package_dir}/weights/{self.context}/dimension_weights.csv"
#         )
#         feature_weights = pd.read_csv(
#             f"{package_dir}/weights/{self.context}/feature_weights.csv"
#         )
#         weights = pd.concat([feature_weights, dimension_weights])[
#             ["feature", "dimension", "weight"]
#         ]
#         return weights

#     def fit_transform(self, bundles: Union[pd.DataFrame, list]) -> pd.DataFrame:
#         """Extends sklearn syntax"""
#         if type(bundles) == list:
#             bundles = pd.DataFrame(bundles)

#         if self.context == "systolic":
#             scored_bundles = self._base_transform(bundles)
#         else:
#             scored_bundles = self._alt_transform(bundles)

#         scored_bundles = scored_bundles.sort_values(
#             ["group", "fitness_score"], ascending=False
#         ).reset_index(drop=True)
#         print(f"Context: {self.context}")
#         print(scored_bundles["group"].value_counts())
#         return scored_bundles

#     @staticmethod
#     def _base_transform(bundles, tolerance=7):
#         """ "
#         MinMx, then parse to 0-100 int
#         """

#         bundles["y"] = bundles["entry"].apply(lambda x: len(x))
#         bundles[["y"]] = MinMaxScaler().fit_transform(bundles[["y"]])
#         bundles["fitness_score"] = bundles["y"].apply(lambda x: int(x * 100))
#         bundles["group"] = bundles["fitness_score"].apply(
#             lambda x: "pass" if x > tolerance else "fail"
#         )

#         bundles = bundles.sort_values(
#             ["group", "fitness_score"], ascending=False
#         ).reset_index(drop=True)
#         return bundles

#     @staticmethod
#     def _alt_transform(bundles):
#         """ "
#         StandardScaler, capped, with minmax, then parse to 0-100 int
#         """

#         bundles["y"] = bundles["entry"].apply(lambda x: len(x))
#         bundles[["y"]] = StandardScaler().fit_transform(bundles[["y"]])

#         def _cap_z(x, sigma=3):
#             if x > sigma:
#                 return sigma
#             elif x < (-1 * sigma):
#                 return -1 * sigma
#             else:
#                 return x

#         bundles["y"] = bundles["y"].apply(_cap_z)
#         bundles[["y"]] = MinMaxScaler().fit_transform(bundles[["y"]])
#         bundles["fitness_score"] = bundles["y"].apply(lambda x: int(x * 100))
#         bundles["group"] = bundles["fitness_score"].apply(
#             lambda x: "pass" if x > 7 else "fail"
#         )

#         return bundles

#     def visualize(self, scored_bundles: pd.DataFrame) -> None:
#         scored_bundles = self.fit_transform(scored_bundles)
#         px.histogram(
#             scored_bundles.sort_values("group"),
#             x="score",
#             facet_col="group",
#             title=f'{dict(scored_bundles["group"].value_counts())}',
#         ).show()
