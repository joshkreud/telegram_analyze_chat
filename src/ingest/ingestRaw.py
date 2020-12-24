from pathlib import Path
import pandas as pd
import json
import src.paths as paths
import numpy as np
import io


def load() -> pd.DataFrame:
    importpath: Path = paths.raw_data_path()
    raw = io.open(importpath).read()
    in_json = json.loads(raw)
    imp_df = pd.DataFrame(in_json["messages"])
    imp_df.set_index("id", inplace=True)
    imp_df["date"] = pd.to_datetime(imp_df["date"])
    imp_df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

    return imp_df