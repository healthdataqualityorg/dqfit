
import plotly.express as px
import pandas as pd

from dqfit.preprocessing.fhir_transform import transform_bundles
from dqfit.query import weights_query


class DQIModel:
    def __init__(self, context: list = ["BCSE", "COLE"]) -> None:
        self.context = context

    @staticmethod
    def set_pass_fail(X, threshold=2):
        if X >= threshold:
            return "pass"
        else:
            return "fail"

    def fit(self, bundles):
        # hmm do I like this name better?
        RF = transform_bundles(bundles)

        def _get_patient_features(resource_level_features):
            # tidy this up
            df = resource_level_features.copy()
            df = df[df["resource_type"] == "Patient"].dropna(how="all", axis=1)
            # display(PF)
            df["dim_type"] = "resource_type"
            df["dim_key"] = "Patient"
            df["dim_weight"] = 1
            return df

        dim_weights = weights_query(context=self.context)
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
            .agg(fit_score=("dim_score", "sum"))
            .reset_index()
        )
        fitness_scores["outcome"] = fitness_scores["fit_score"].apply(
            self.set_pass_fail
        )
        fitness_scores["outcome"] = pd.Categorical(
            fitness_scores["outcome"], ["pass", "fail"])
        fitness_scores = fitness_scores.sort_values(["context", "outcome", "fit_score"], ascending=[
                                                    True, True, False]).reset_index(drop=True)
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
            cohort_outcomes.sort_values(
                ["context", "outcome"], ascending=True),
            x="context",
            y="count",
            color="outcome",
            title=f"Cohort Outcomes",
        ).show()

    # def cohort_level_scores(self):
    #     fitness_scores
    #     cohort_outcomes = fitness_scores.groupby(['context','outcome']).agg(count=("outcome","count")).reset_index()
    #     cohort_outcomes

