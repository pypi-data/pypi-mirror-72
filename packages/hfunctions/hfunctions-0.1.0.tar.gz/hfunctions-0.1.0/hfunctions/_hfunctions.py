import pandas as pd
import random

__all__ = ["create_sample_df", "random_actual_prediction"]


def create_sample_df():
    df = pd.read_csv('../data/sample_df.csv')
    return df


def random_actual_prediction(n_classes=2, size=100, random_seed=42):
    random.seed(random_seed)
    classes = list(range(n_classes))
    y_actual = random.choices(classes, k=size)
    y_pred = random.choices(classes, k=size)
    return y_actual, y_pred
