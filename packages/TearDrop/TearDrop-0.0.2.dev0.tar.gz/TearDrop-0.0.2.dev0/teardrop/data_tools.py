import pandas as pd
import os


def load_headbrain() -> pd.DataFrame:
    path = os.path.join(os.path.dirname(__file__), r'datasets/headbrain.csv')
    df = pd.read_csv(path)
    return df


def load_dinos() -> pd.DataFrame:
    path = os.path.join(os.path.dirname(__file__), r'datasets/dinos.csv')
    df = pd.read_csv(path)
    return df
