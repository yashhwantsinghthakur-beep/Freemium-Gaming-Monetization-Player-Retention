import pandas as pd

def calculate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = ["Age", "SessionCount", "AverageSessionLength", "InAppPurchaseAmount", "FirstPurchaseDaysAfterInstall"]
    valid_cols = [c for c in num_cols if c in df.columns]
    if df.empty or len(valid_cols) == 0:
        return pd.DataFrame()
    return df[valid_cols].corr().round(3)