import plotly.express as px
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from typing import Union

# could be an abstraction
class DQIModel:

    def __init__(self, context="weights_dir") -> None:
        """ Does stuff """
        self.context = context
    
    def fit_transform(self, bundles: Union[pd.DataFrame,list]) -> pd.DataFrame:
        """ Extends sklearn syntax """
        if type(bundles) == list:
            bundles = pd.DataFrame(bundles)

        if self.context == "systolic":
            return self._base_transform(bundles)
        else:
            return self._alt_transform(bundles)

    @staticmethod
    def _base_transform(bundles):
        """" 
            StandardScaler, capped, with minmax, then parse to 0-100 int
        """

        bundles["y"] = bundles["entry"].apply(lambda x: len(x))
        bundles[["y"]] = StandardScaler().fit_transform(bundles[["y"]])
        def _cap_z(x, sigma=3):
            if x > sigma:
                return sigma
            elif x < (-1 * sigma):
                return (-1 * sigma)
            else:
                return x
        bundles['y'] = bundles['y'].apply(_cap_z)
        bundles[["y"]] = MinMaxScaler().fit_transform(bundles[["y"]])
        bundles["score"] = bundles["y"].apply(lambda x: int(x * 100))
        bundles["group"] = bundles["score"].apply(lambda x: "pass" if x > 7 else "fail")
        return bundles

    @staticmethod
    def _alt_transform(bundles):
        """" 
            Like the other one but different
        """

        bundles["y"] = bundles["entry"].apply(lambda x: len(x))
        bundles[["y"]] = MinMaxScaler().fit_transform(bundles[["y"]])
        bundles["score"] = bundles["y"].apply(lambda x: int(x * 100))
        bundles["group"] = bundles["score"].apply(lambda x: "pass" if x > 7 else "fail")
        return bundles

    def visualize(self, scored_bundles: pd.DataFrame) -> None:
        scored_bundles = self.fit_transform(scored_bundles)
        px.histogram(
            scored_bundles.sort_values("group"),
            x="score",
            facet_col="group",
            title=f'{dict(scored_bundles["group"].value_counts())}',
        ).show()
