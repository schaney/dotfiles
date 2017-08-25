# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys, math

def progress(value,  length=40, vmin=0.0, vmax=1.0):
    """
    Text progress bar

    Parameters
    ----------
    value : float
        Current value to be displayed as progress

    vmin : float
        Minimum value

    vmax : float
        Maximum value

    length: int
        Bar length (in character)

    title: string
        Text to be prepend to the bar
    """
    # Block progression is 1/8
    leftpad="▕"
    rightpad=" "
    blocks = ["", "▏","▎","▍","▌","▋","▊","▉","█"]
    vmin = vmin or 0.0
    vmax = vmax or 1.0

    # Normalize value
    value = min(max(value, vmin), vmax)
    value = (value-vmin)/float(vmax-vmin)

    v = value*length
    # integer part
    x = int(math.floor(v))
    # fractional part
    y = v - x
    base = 0.125      # 0.125 = 1/8
    prec = 3
    i = int(round(base*math.floor(float(y)/base),prec)/base)
    bar = "█"*x + blocks[i]
    n = length-len(bar.decode("utf-8"))
    bar = leftpad + bar + " "*n

    sys.stdout.write(bar)
    sys.stdout.flush()

progress(float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
