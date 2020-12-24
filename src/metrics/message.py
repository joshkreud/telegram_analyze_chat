import pandas as pd
import numpy as np
import re


def conv_hour_dec(time: float) -> str:
    hours = int(time)
    minutes = (time * 60) % 60
    seconds = (time * 3600) % 60

    return "%d:%02d.%02d" % (hours, minutes, seconds)


def process_spec_types(df_in: pd.DataFrame) -> pd.DataFrame:
    mask_types = df_in["text"].astype(str).str.startswith("[{'type': ", na=False)

    dic_type = df_in[mask_types]["text"].map(lambda x: x[0])
    specType = "Special_" + dic_type.map(lambda x: x["type"])
    df_in.loc[mask_types, "media_type"] = specType

    specvalue = dic_type.map(lambda x: x["text"])
    df_in.loc[mask_types, "Spec_Value"] = specvalue

    spectext = df_in[mask_types]["text"].map(lambda x: x[1] if len(x) > 1 else "")
    spectext.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    spectext.dropna(inplace=True)
    df_in.loc[mask_types, "text"] = spectext
    return df_in


def msg_type(df: pd.DataFrame):
    choices = ["Text Only", "Photo with Text"]
    conditions = [
        ((~df["text"].isna()) & (df[["file", "photo", "sticker_emoji"]].isna().all(1))),
        (~df[["text", "photo"]].isna().all(1)),
    ]
    np_res = np.select(conditions, choices, default=np.NaN)
    pd_res = pd.Series(np_res, index=df.index)
    pr_clean = pd_res.replace("nan", np.NaN)
    org_type = df["media_type"].copy()
    org_type.update(pr_clean)
    return org_type


def text_len(df: pd.DataFrame) -> pd.DataFrame:
    return df["text"].str.split().str.len()


def get_text(ser: pd.Series) -> str:
    filter_na = ser[~ser.isna()]
    msg_list = filter_na.to_list()
    only_text = [x for x in msg_list if type(x) is str]
    raw_text = "\n".join(only_text)
    arr_newline = raw_text.replace("\\n", "\n").split("\n")
    join_newline = (" ").join(arr_newline)
    multiwhitespace = re.sub(" +", " ", join_newline)
    re_colon = re.sub('(XD|:O|:D|:|!|"|\(|\)|\?)', "", multiwhitespace)
    no_emoji = deEmojify(re_colon)
    return no_emoji


def emoji_regex_pattern():
    return re.compile(
        pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )


def deEmojify(text):
    return emoji_regex_pattern().sub(r"", text)
