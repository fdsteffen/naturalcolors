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
import pandas as pd
import seaborn as sns
import json
import os

# seaborn settings
sns.set_style('white')
sns.set_context("notebook")
sns.set(font='Arial')

package_directory = os.path.dirname(os.path.abspath(__file__))


def set_ticksStyle(x_size=4, y_size=4, x_dir='in', y_dir='in'):
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
    sns.set_style('ticks', {'xtick.major.size': x_size, 'ytick.major.size': y_size, 'xtick.direction': x_dir, 'ytick.direction': y_dir})


def _load_colors(filename='naturalcolors.json'):
    """
    Load the colors from a json file 

    Parameters
    ----------
    filename : str
    """
    with open(os.path.join(package_directory, filename)) as f:
        colors_rgb = np.array(json.load(f))
        return np.hstack((colors_rgb / 255, np.ones((24, 1))))


def naturalcolors():
    """
    Wrapper for naturalcolors which builds the colormap from a loaded json file
    """
    colors = _load_naturalcolors()
    return make_colormap(colors, 'naturalcolors')


def make_colormap(colors, name='newcolormap'):
    """
    Build a listed and a linear segmented colormap from a list of colors

    Parameters
    ----------
    colors : array_like
    name : str
    """
    listedCmap = mpl.colors.ListedColormap(colors, name=name + '_list')
    linearSegmentedCmap = _listed2linearSegmentedColormap(listedCmap, name)
    return listedCmap, linearSegmentedCmap


def _listed2linearSegmentedColormap(listedCmap, name='newcolormap'):
    """
    Convert a listed to a linear segmented colormap

    Parameters
    ----------
    listedCmap : listed_colormap
    name : str
    """
    c = np.array(listedCmap.colors)
    x = np.linspace(0, 1, len(c))
    cdict = cdict = {'red': np.vstack((x, c[:, 0], c[:, 0])).T,
                     'green': np.vstack((x, c[:, 1], c[:, 1])).T,
                     'blue': np.vstack((x, c[:, 2], c[:, 2])).T}
    return mpl.colors.LinearSegmentedColormap(name=name, segmentdata=cdict, N=256)


def get_colors(cmap, n):
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
        print('The colormap \"{}\"" is built from {:d} colors. Those are listed below'.format(cmap.name, cmap.N))
        n = cmap.N
    return cmap(np.linspace(0, 1, n))


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
    with sns.axes_style('white'):
        set_ticksStyle()
        ax = plt.subplot(111, projection='polar')
        if n > cmap.N:
            print('The colormap \"{}\"" is built from {:d} colors'.format(cmap.name, cmap.N))
            n = cmap.N
        theta = np.linspace(0, 2 * np.pi - 2 * np.pi / n, n)
        r = [1] * n
        ax.scatter(theta, r, c=theta, s=area, cmap=cmap)
        ax.axis('off')
        ax.grid(which='major', visible=False)
        ax.text(0, 0, name, va='center', ha='center', fontsize=12)


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
    with sns.axes_style('white'):
        set_ticksStyle()
        fig, ax = plt.subplots(figsize=(4, 1))
        fig.subplots_adjust(bottom=0.7)
        ax.set_axis_off()
        mpl.colorbar.ColorbarBase(ax, cmap=cmap, orientation='horizontal')
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3] / 2.
        fig.text(x_text, y_text, name, va='center', ha='right', fontsize=12)
