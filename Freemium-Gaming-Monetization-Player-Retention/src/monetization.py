import pandas as pd

def calculate_arpu(df: pd.DataFrame) -> float:
    if df.empty or "InAppPurchaseAmount" not in df.columns:
        return 0.0
    return float(df["InAppPurchaseAmount"].sum() / df["UserID"].nunique())

def segment_revenue_contribution(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["SpendingSegment", "TotalRevenue", "UserCount", "RevenueSharePct"])
    summary = df.groupby("SpendingSegment").agg(
        TotalRevenue=("InAppPurchaseAmount", "sum"),
        MeanSpend=("InAppPurchaseAmount", "mean"),
        UserCount=("UserID", "nunique")
    ).reset_index()
    
    tot_rev = summary["TotalRevenue"].sum()
    summary["RevenueSharePct"] = (summary["TotalRevenue"] / tot_rev * 100).round(2) if tot_rev > 0 else 0.0
    return summary.sort_values(by="TotalRevenue", ascending=False)

def genre_monetization_depth(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return df.pivot_table(
        index="GameGenre",
        columns="SpendingSegment",
        values="InAppPurchaseAmount",
        aggfunc="mean"
    ).round(2).fillna(0).reset_index()