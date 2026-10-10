"""Loading raw and external data into tidy tables."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
EXTERNAL_DIR = DATA_DIR / "external"
PROCESSED_DIR = DATA_DIR / "processed"


def load_csv(path: Path, **kwargs) -> pd.DataFrame:
    """Read a CSV, raising a clear error if the file has not been downloaded yet."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Download it first; see data/README.md."
        )
    return pd.read_csv(path, **kwargs)
