import pandas as pd

def compute_conversion_latency(df: pd.DataFrame) -> pd.Series:
    """Analyze distribution of days taken from install to first IAP."""
    return df["FirstPurchaseDaysAfterInstall"].describe()