"""
Get evaluation metrics from a DataFrame.

The DataFrame must contain the following columns:

* ["nf"] with the predictions as a dictionary.
   The dictionary has 2 keys: "top1" and "top5"
* ["44_plus_l3"] with the true value #todo: change
"""

from typing import Tuple
import pandas as pd
import numpy as np

from sklearn.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    multilabel_confusion_matrix,
    precision_recall_fscore_support,
)

from operator import itemgetter

# TODO: new way to get the names! IMPORTANT!
# I need to have control over the images storage before doing this
# df_hotdog_chill = pd.read_csv("../csvs/hotdog_43plus.csv")
# to_name = dict(zip(df_hotdog_chill["43plus_L3"], df_hotdog_chill["43p_L3_name"]))
# to_name_inv = {k: v for v, k in to_name.items()}
# to_name["T69.1"] = "Chilblains"


def get_topk_dataframe(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    Process DataFrame before getting the metrics.
    """

    df = df.copy()

    df["top1"] = df["results"].apply(itemgetter("top1"))
    df["top5"] = df["results"].apply(itemgetter("top5"))

    df["top5_mode"] = df.apply(lambda x: get_if_top(x["44_plus_l3"], x["top5"]), axis=1)

    df = df.rename(mappeer={"top5": "top5_all", "top5_mode": "top5"}, axis=1)

    res = df[["label", "top1", "top5"]]

    return res


def tn(matrix):
    """Get true negatives."""
    return matrix[0, 0]


def fp(matrix):
    """Get false positives."""
    return matrix[0, 1]


def fn(matrix):
    """Get false negatives."""
    return matrix[1, 0]


def tp(matrix):
    """Get true positives."""
    return matrix[1, 1]


def get_topk_dictionary(res: pd.core.frame.DataFrame, topk: str = "top1") -> dict:
    """Get topk metrics dictionary."""

    report_dict = classification_report(
        y_true=res["44_plus_l3"], y_pred=res[topk], output_dict=True
    )

    return report_dict


def get_overall_metrics(report_dict: dict) -> Tuple[pd.core.frame.DataFrame, dict]:
    """Extract DataFrame and overall metrics from report dictionary."""

    report_dict = report_dict.copy()

    overall_metrics = {}  # create dictionary

    for metric in ["accuracy", "macro avg", "weighted avg"]:
        overall_metrics[metric] = report_dict[metric]
        del report_dict[metric]

    report_names = {to_name[k]: v for k, v in report_dict.items()}
    report_dataframe = pd.DataFrame(report_names).T
    return report_dataframe, overall_metrics


def fill_all_metrics(
    results: pd.core.frame.DataFrame, report_table: pd.core.frame.DataFrame,
) -> pd.core.frame.DataFrame:
    """Fill DataFrame with all the metrics."""

    res = results.copy()

    report_table = report_table.copy()

    all_matrix = multilabel_confusion_matrix(
        y_true=res["44_plus_l3"],
        y_pred=res["top1"],
        labels=[to_name_inv[name] for name in report_table.index.to_list()],
    )

    report_table["true_positive"] = [tp(m) for m in all_matrix]
    report_table["false_positive"] = [fp(m) for m in all_matrix]
    report_table["false_negative"] = [fn(m) for m in all_matrix]
    report_table["true_negative"] = [tn(m) for m in all_matrix]

    return report_table


def write_dataframe(df: pd.core.frame.DataFrame) -> None:
    """Write DatFrame to file."""

    pass


def get_if_top(true: str, top5_preds: list) -> str:
    """
    Check if the true label is in one of the top 5 results.

    If the tru label is in the top 5,  return the label, if not, it returns the top1, which we know is false.
    """
    if true in top5_preds:
        return true

    return top5_preds[0]


def get_top5_mode(df: pd.DataFrame) -> pd.DataFrame:
    """Get single top5 prediction."""

    restop = df.copy()

    restop["top5_mode"] = restop.apply(
        lambda x: get_if_top(x["44_plus_l3"], x["top5"]), axis=1
    )


# TODO:
# add argparse
# wire everything together
