import pandas as pd

import os.path
from pathlib import Path
import logging
import json

IMPORT_PATH = "./in/"


def get_export_path() -> Path:
    p = Path(IMPORT_PATH + "result.json")
    if not p.exists():
        raise FileNotFoundError
    return p


def import_data() -> pd.DataFrame:
    importpath: Path = get_export_path()

    with open(importpath) as f:
        in_json = json.load(f)

    return pd.DataFrame(in_json["messages"])


def main():
    main_df = import_data()
    main_df.to_excel("./out/Raw.xlsx")


if __name__ == "__main__":
    logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
    main()