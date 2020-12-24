# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import os
import sys
path_parent = os.path.dirname(sys.path[0])
os.chdir(path_parent)

# +
# %load_ext autoreload
# %autoreload 2

import src
import pandas as pd
import numpy as np
# -

raw_df = src.ingest.raw.load()

raw_df.to_excel(src.paths.processed_data_path() / "01_Import.xlsx")

display(raw_df['date'].min())
display(raw_df['date'].max())
raw_df['from'].value_counts()

proc_df = raw_df.copy()
proc_df = src.metrics.message.process_spec_types(proc_df)
proc_df['msg_type'] = src.metrics.message.msg_type(proc_df)
proc_df['text_len'] =  src.metrics.message.text_len(proc_df)

proc_df['msg_type'].value_counts(dropna=False)

proc_df.to_excel(src.paths.processed_data_path() / "02_Processed.xlsx")

voice_msg_grp = proc_df[proc_df['msg_type']=='voice_message'].groupby(['from'])
display(voice_msg_grp['duration_seconds'].count())
voice_duration = voice_msg_grp['duration_seconds'].sum()/60/60
voice_duration.apply(src.metrics.message.conv_hour_dec)

# +
dates = proc_df["date"].dt

textlen = proc_df.groupby([proc_df['from'],dates.year,dates.month,dates.isocalendar()['week']])['text_len'].mean().unstack('from')
textlen.plot(kind="bar",stacked=False,figsize=(30,6),title="Mean Message length per Week")

textlen = proc_df.groupby([dates.year,dates.month,dates.isocalendar()['week']])['from'].value_counts().unstack('from')
textlen.plot(kind="bar",stacked=False,figsize=(30,6),title="Message count per Week")

# +
from PIL import Image
import matplotlib.pyplot as plt

stopwords = src.visualisation.wordcloud.stopwords()

participants = proc_df['from'].dropna().unique()

mask_part1 = (proc_df['from']==participants[0])
text1 = src.metrics.message.get_text(proc_df.loc[ mask_part1,'text'])
wc1 = src.visualisation.wordcloud.mask_word_cloud(text1,src.paths.data_path() /'IMG_Part_1.png',stopwords=stopwords)

mask_part2 = (proc_df['from']==participants[1])
text2 = src.metrics.message.get_text(proc_df.loc[ mask_part2,'text'])
wc2 = src.visualisation.wordcloud.mask_word_cloud(text1, src.paths.data_path() /'IMG_Part_2.png',stopwords=stopwords)

raw_img = np.array(Image.open(src.paths.data_path() /'IMG.png'))
cont_img = np.array(Image.open(src.paths.data_path() /'IMG_Background.png'))
# -


plt.figure(figsize=(50, 50))
plt.axis('off')
wc1 = wc1.recolor(colormap='terrain')
wc2 = wc2.recolor(colormap='rainbow')
plt.imshow(cont_img)
plt.imshow(raw_img,alpha=0.4)
plt.imshow(wc1,interpolation="bilinear")
plt.imshow(wc2,interpolation="bilinear")
plt.savefig(src.paths.output_path() / 'WordCloud_3.png', transparent=True)

proc_df.groupby([ proc_df['from'],dates.weekday,dates.hour,dates.minute])['text_len'].mean().unstack([0,1]).plot(stacked=False,figsize=(30,20))

textlen_time = proc_df.groupby([ proc_df['from'],dates.day,dates.hour,dates.minute])['text_len'].mean().unstack(['from'])
textlen_time.plot(title='Mean Textlength by Hour of day',stacked=False,figsize=(30,20))

msgcount_time = proc_df.groupby([proc_df['from'],dates.hour,dates.minute])['from'].count().unstack('from')
msgcount_time.plot(title='MsgCount by Hour of day',stacked=False,figsize=(30,20))
