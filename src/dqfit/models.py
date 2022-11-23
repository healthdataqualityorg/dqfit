import plotly.express as px
import pandas as pd

from dqfit.preprocessing import ResourceFeatures
from dqfit.query import dim_weights_query


class DQIModel:
    def __init__(self, context="IMAE") -> None:
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
            df = resource_level_features.copy()
            df = df[df["resource_type"] == "Patient"].dropna(how="all", axis=1)
            # display(PF)
            df["dim_type"] = "resource_type"
            df["dim_key"] = "Patient"
            df["dim_weight"] = 1
            # WPF = PF # "Weighted Patient Feature"
            return df

        dim_weights = dim_weights_query(self.context)
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
    def visualize_scores(scores):
        
        print(scores['outcome'].value_counts(normalize=True))
        cohort_outcomes = (
            scores.groupby(["context", "outcome"])
            .agg(count=("outcome", "count"))
            .reset_index()
        )
        
        px.bar(
            cohort_outcomes.sort_values(["outcome","context"], ascending=False),
            x="context",
            y="count",
            color="outcome",
            title=f"Cohort Outcomes",
        ).show(renderer='notebook')

    # def cohort_level_scores(self):
    #     fitness_scores
    #     cohort_outcomes = fitness_scores.groupby(['context','outcome']).agg(count=("outcome","count")).reset_index()
    #     cohort_outcomes
