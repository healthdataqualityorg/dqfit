import pandas as pd
import plotly.express as px


def draw_score_distribution(scored_bundles: pd.DataFrame) -> None:
    px.histogram(
        scored_bundles.sort_values("group"),
        x="score",
        facet_col="group",
        title=f'{dict(scored_bundles["group"].value_counts())}',
    ).show()


def __main__():
    draw_score_distribution()
