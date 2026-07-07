from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/car_data.xlsx")


def load_car_data() -> pd.DataFrame:
    """
    Load the automobile dataset.
    """

    return pd.read_excel(DATA_PATH)