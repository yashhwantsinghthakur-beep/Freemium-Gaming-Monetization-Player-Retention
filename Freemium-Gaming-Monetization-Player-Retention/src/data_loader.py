from pathlib import Path
from typing import Optional, Tuple
import pandas as pd

# Root directory of the repository (parent of 'src/')
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_data_path(filename: str = "mobile_game_inapp_purchases.csv") -> Path:
    """Finds the dataset across common relative directory locations."""
    search_paths = [
        PROJECT_ROOT / "data" / "raw" / filename,
        PROJECT_ROOT / "data" / filename,
        PROJECT_ROOT / filename,
        Path.cwd() / "data" / "raw" / filename,
        Path.cwd() / "data" / filename,
        Path.cwd() / filename,
    ]
    
    for candidate in search_paths:
        if candidate.exists():
            return candidate
            
    # Default fallback path
    return PROJECT_ROOT / "data" / "raw" / filename

def load_raw_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Loads raw dataset from CSV or returns empty DataFrame on failure."""
    path = filepath or get_data_path()
    
    if not Path(path).exists():
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. Ensure 'mobile_game_inapp_purchases.csv' is tracked in Git."
        )
        
    return pd.read_csv(path)

def clean_game_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Imputes missing values and formats types."""
    if df.empty:
        return df.copy(), df.copy()
        
    df_clean = df.copy()
    
    # Impute missing demographics and categorical fields
    if "Age" in df_clean.columns:
        df_clean["Age"] = df_clean["Age"].fillna(df_clean["Age"].median())
    if "Gender" in df_clean.columns:
        df_clean["Gender"] = df_clean["Gender"].fillna("Unknown")
    if "Country" in df_clean.columns:
        df_clean["Country"] = df_clean["Country"].fillna("Unknown")
    if "Device" in df_clean.columns:
        df_clean["Device"] = df_clean["Device"].fillna("Other")
    if "GameGenre" in df_clean.columns:
        df_clean["GameGenre"] = df_clean["GameGenre"].fillna("Other")
    
    if "LastPurchaseDate" in df_clean.columns:
        df_clean["LastPurchaseDate"] = pd.to_datetime(df_clean["LastPurchaseDate"], errors="coerce")
        
    if "InAppPurchaseAmount" in df_clean.columns:
        paying_df = df_clean[df_clean["InAppPurchaseAmount"] > 0].copy()
        f2p_df = df_clean[df_clean["InAppPurchaseAmount"].isna() | (df_clean["InAppPurchaseAmount"] == 0)].copy()
    else:
        paying_df = df_clean.iloc[0:0].copy()
        f2p_df = df_clean.copy()
        
    return paying_df, f2p_df

def filter_gaming_dataset(
    df: pd.DataFrame,
    genres: Optional[list] = None,
    segments: Optional[list] = None,
    devices: Optional[list] = None,
    countries: Optional[list] = None
) -> pd.DataFrame:
    """Filters dataset based on selected sidebar criteria."""
    filtered = df.copy()
    
    if genres and "GameGenre" in filtered.columns:
        filtered = filtered[filtered["GameGenre"].isin(genres)]
    if segments and "SpendingSegment" in filtered.columns:
        filtered = filtered[filtered["SpendingSegment"].isin(segments)]
    if devices and "Device" in filtered.columns:
        filtered = filtered[filtered["Device"].isin(devices)]
    if countries and "Country" in filtered.columns:
        filtered = filtered[filtered["Country"].isin(countries)]
        
    return filtered