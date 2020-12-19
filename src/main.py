import pandas as pd

import os.path
from pathlib import Path
import logging
import json
import numpy as np

IMPORT_PATH = "./in/"
EXPORT_PATH = "./out/"


def get_import_path() -> Path:
    p = Path(IMPORT_PATH + "result.json")
    if not p.exists():
        raise FileNotFoundError
    return p


def get_export_path() -> Path:
    path = Path(EXPORT_PATH)
    path.mkdir(parents=True, exist_ok=True)
    return path


def import_data() -> pd.DataFrame:
    importpath: Path = get_import_path()

    with open(importpath) as f:
        in_json = json.load(f)
    imp_df = pd.DataFrame(in_json["messages"])
    imp_df.set_index("id", inplace=True)
    imp_df["date"] = pd.to_datetime(imp_df["date"])

    return imp_df


def df_msg_type(df: pd.DataFrame):
    choices = ["Text Only", "Photo with Text"]
    conditions = [
        ((~df["text"].isna()) & (df[["file", "photo", "sticker_emoji"]].isna().all(1))),
        (df[["text", "photo"]].isna().all(1)),
    ]
    np_res = np.select(conditions, choices, default=np.NaN)
    pd_res = pd.Series(np_res, index=df.index)
    pr_clean = pd_res.replace("nan", np.NaN)
    return pr_clean


def df_text_metrics(df: pd.DataFrame) -> pd.DataFrame:
    textlen = df["text"].str.split().str.len()


def main():
    main_df = import_data()
    out_dir: Path = Path("./out/")

    out_dir.mkdir(parents=True, exist_ok=True)

    group_user = main_df.groupby("from")
    print(main_df.value_counts("from"))


if __name__ == "__main__":
    logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
    main()