import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.ndimage import gaussian_gradient_magnitude
from wordcloud import ImageColorGenerator
import re
import string


def mask_word_cloud(text: str, img_path: str, **kwargs) -> WordCloud:
    # load image. This has been modified in gimp to be brighter and have more saturation.
    img_1 = np.array(Image.open(img_path))
    # subsample by factor. Very lossy but for a wordcloud we don't really care.
    # img_1 = img_1[::2, ::2]

    # create mask  white is "masked out"
    img_1_mask = img_1.copy()
    img_1_mask[img_1_mask.sum(axis=2) == 0] = 255

    # some finesse: we enforce boundaries between colors so they get less washed out.
    # For that we do some edge detection in the image
    edges = np.mean(
        [gaussian_gradient_magnitude(img_1_mask[:, :, i] / 255.0, 2) for i in range(3)],
        axis=0,
    )
    img_1_mask[edges > 0.08] = 255

    # create wordcloud. A bit sluggish, you can subsample more strongly for quicker rendering
    # relative_scaling=0 means the frequencies in the data are reflected less
    # acurately but it makes a better picture
    wc = WordCloud(
        max_words=500,
        mask=img_1_mask,
        relative_scaling=0,
        max_font_size=160,
        min_font_size=8,
        min_word_length=2,
        repeat=False,
        background_color="rgba(255, 255, 255, 0)",
        mode="RGBA",
        **kwargs,
    )

    # generate word cloud
    wc.generate(text.upper())
    return wc


def image_color_func(path: str):
    colormap = np.array(Image.open(path))
    return ImageColorGenerator(colormap)


def stopwords(append: set = set()):
    stopfile = open("./resources/stopwords.txt", "r")
    res = [line.replace("\n", "") for line in stopfile.readlines()]
    res = set(res)
    if append:
        res = res | append
    return res
