from pathlib import Path
import pandas as pd
import json
import src.paths as paths


def load() -> pd.DataFrame:
    importpath: Path = paths.raw_data_path()

    with open(importpath) as f:
        in_json = json.load(f)
    imp_df = pd.DataFrame(in_json["messages"])
    imp_df.set_index("id", inplace=True)
    imp_df["date"] = pd.to_datetime(imp_df["date"])

    return imp_df