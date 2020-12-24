from pathlib import Path

DATA_PATH = "./data/"
OUTPUT_PATH = "./outputs/"


def data_path() -> Path:
    p = Path(DATA_PATH)
    return p


def raw_data_path() -> Path:
    p = Path(DATA_PATH)
    p = p / "raw/result.json"
    if not p.exists():
        raise FileNotFoundError
    return p


def processed_data_path() -> Path:
    path = Path(DATA_PATH)
    path = path / "processed"
    path.mkdir(parents=True, exist_ok=True)
    return path


def output_path() -> Path:
    return Path(OUTPUT_PATH)