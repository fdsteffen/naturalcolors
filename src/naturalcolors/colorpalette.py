#!/usr/bin/env python3

"""
Make a custom colormap from a list of colors

References
----------

How to create a colormap: 

https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import collections
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
DEFAULT_COLORMAP = Path(PKG_DIR).joinpath("colormaps.json")

# seaborn settings
sns.set_style("white")
sns.set_context("notebook")
sns.set_theme(font="Arial")

package_directory = os.path.dirname(os.path.abspath(__file__))


def set_ticksStyle(x_size=4, y_size=4, x_dir="in", y_dir="in"):
    """
    Ticks settings for plotting

    Parameters
    ----------
    x_size : float
             length of x-ticks
    y_size : float
             length of y-ticks
    x_dir : str, ('in' or 'out')
            inward or outward facing x-ticks
    y_dir : str, ('in' or 'out')
            inward or outward facing y-ticks
    """
    sns.set_style(
        "ticks",
        {
            "xtick.major.size": x_size,
            "ytick.major.size": y_size,
            "xtick.direction": x_dir,
            "ytick.direction": y_dir,
        },
    )


def load_colors(filename=DEFAULT_COLORMAP):
    """
    Load rgba colors from a json file

    Parameters
    ----------
    filename : str
    """
    with open(filename) as f:
        inputcolors = json.load(f)
        for name, colors_rgb in inputcolors.items():
            colors_rgb = np.array(colors_rgb)
            if colors_rgb.shape[1] == 3:
                colors_rgba = np.hstack(
                    (colors_rgb / 255, np.ones((colors_rgb.shape[0], 1)))
                )
            else:
                colors_rgba = colors_rgb
            inputcolors[name] = colors_rgba
        return inputcolors


def _scramble_pop(d):
    """
    Reorder the colors as [first, last, second, second but last, ...]
    """
    try:
        while True:
            yield d.popleft()
            yield d.pop()
    except IndexError:
        pass


def get_cmap(name=None, colormap_filename=DEFAULT_COLORMAP):
    """
    Return the selected LinearSegmentedColormap or a dictionary of all colormaps registered in colormap_filename

    Parameters
    ----------
    name : str
    colormap_filename : str
                        path to a json file encoding a dictionary of colors which define custom colormaps
    """
    default_inputcolors = load_colors(colormap_filename)
    default_cmaps = {
        key: make_colormap(colors, key) for key, colors in default_inputcolors.items()
    }
    if name is None:
        return default_cmaps
    else:
        try:
            return default_cmaps[name][1]
        except KeyError:
            print(
                'Colormap "{}" is not yet in the list of registered colormaps.'
                "You may add your input colors to colormaps.json".format(name)
            )
            return None


def naturalcolors():
    """
    Wrapper for naturalcolors map
    """
    default_cmaps = get_cmap()
    return default_cmaps["naturalcolors"]


def list_cmaps():
    """
    List all available colormaps
    """
    return list(get_cmap().keys())


def make_colormap(colors, name="newcolormap"):
    """
    Build a listed and a linear segmented colormap from a list of colors

    Parameters
    ----------
    colors : array_like
    name : str
    """
    listedCmap = mpl.colors.ListedColormap(colors, name=name + "_list")
    linearSegmentedCmap = _listed2linearSegmentedColormap(listedCmap, name)
    return listedCmap, linearSegmentedCmap


def _listed2linearSegmentedColormap(listedCmap, name="newcolormap"):
    """
    Convert a listed to a linear segmented colormap

    Parameters
    ----------
    listedCmap : listed_colormap
    name : str
    """
    c = np.array(listedCmap.colors)
    x = np.linspace(0, 1, len(c))
    cdict = cdict = {
        "red": np.vstack((x, c[:, 0], c[:, 0])).T,
        "green": np.vstack((x, c[:, 1], c[:, 1])).T,
        "blue": np.vstack((x, c[:, 2], c[:, 2])).T,
    }
    return mpl.colors.LinearSegmentedColormap(name=name, segmentdata=cdict, N=256)


def get_colors(cmap, n, scramble=False):
    """
    Extract n colors from a colormap

    Parameters
    ----------
    cmap : colormap or str
           listed / linear segmented colormap or the name of a registered colormap
    n : int
        number of colors to extract from the colormap
    """
    if type(cmap) is str:
        name = cmap
        cmap = plt.get_cmap(cmap)
    else:
        name = cmap.name
    if n > cmap.N:
        print(
            'The colormap "{}"" is built from {:d} colors. Those are listed below'.format(
                cmap.name, cmap.N
            )
        )
        n = cmap.N
    colors = cmap(np.linspace(0, 1, n))
    if scramble:
        colors = np.array(list(_scramble_pop(collections.deque(colors))))
    return colors


def drawColorCircle(cmap, n=24, area=200):
    """
    Draw a color circle from the colormap

    Parameters
    ----------
    cmap : colormap or str
           listed / linear segmented colormap or the name of a registered colormap
    n : int
        number of colors to display in the color circle (set n=256 for a continuous circle)
    area : int
           size of the circles to draw
    """
    if type(cmap) is str:
        name = cmap
        cmap = plt.get_cmap(cmap)
    else:
        name = cmap.name
    with sns.axes_style("white"):
        set_ticksStyle()
        ax = plt.subplot(111, projection="polar")
        if n > cmap.N:
            print(
                'The colormap "{}"" is built from {:d} colors'.format(cmap.name, cmap.N)
            )
            n = cmap.N
        theta = np.linspace(0, 2 * np.pi - 2 * np.pi / n, n)
        r = [1] * n
        ax.scatter(theta, r, c=theta, s=area, cmap=cmap)
        ax.axis("off")
        ax.grid(which="major", visible=False)
        ax.text(0, 0, name, va="center", ha="center", fontsize=12)


def drawColorBar(cmap):
    """
    Draw a colorbar from the colormap

    Parameters
    ----------
    cmap : colormap or str
           listed / linear segmented colormap or the name of a registered colormap
    """
    if type(cmap) is str:
        name = cmap
        cmap = plt.get_cmap(cmap)
    else:
        name = cmap.name
    with sns.axes_style("white"):
        set_ticksStyle()
        fig, ax = plt.subplots(figsize=(4, 1))
        fig.subplots_adjust(bottom=0.7)
        ax.set_axis_off()
        mpl.colorbar.ColorbarBase(ax, cmap=cmap, orientation="horizontal")
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3] / 2.0
        fig.text(x_text, y_text, name, va="center", ha="right", fontsize=12)
