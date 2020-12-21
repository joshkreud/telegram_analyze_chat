import pandas as pd
import numpy as np


def msg_type(df: pd.DataFrame):
    choices = ["Text Only", "Photo with Text"]
    conditions = [
        ((~df["text"].isna()) & (df[["file", "photo", "sticker_emoji"]].isna().all(1))),
        (df[["text", "photo"]].isna().all(1)),
    ]
    np_res = np.select(conditions, choices, default=np.NaN)
    pd_res = pd.Series(np_res, index=df.index)
    pr_clean = pd_res.replace("nan", np.NaN)
    return pr_clean


def text_len(df: pd.DataFrame) -> pd.DataFrame:
    return df["text"].str.split().str.len()