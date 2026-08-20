from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

def get_data_path(filename: str, subfolder: str = "raw") -> Path:
    return DATA_DIR / subfolder / filename