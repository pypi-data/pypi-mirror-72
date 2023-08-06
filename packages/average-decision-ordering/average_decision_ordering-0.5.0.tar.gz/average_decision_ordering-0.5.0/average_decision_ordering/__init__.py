#! /usr/bin/env python

import numpy as np
import pandas as pd
import itertools

def heaviside(x):
    return 0.5 * (np.sign(x) + 1)

def norm(x):
    return (x-min(x))/(max(x)-min(x))

def calc_do(fx0, fx1, gx0, gx1):
    def heaviside(x):
        return 0.5 * (np.sign(x) + 1)

    dfx = fx0 - fx1
    dgx = gx0 - gx1
    dos = heaviside(np.multiply(dfx, dgx))
    return dos

def calc_ado(fx, gx, target, n_data=False):
    # normalize input data
    fx = norm(fx)
    gx = norm(gx)

    if not n_data:
        n_data = len(fx)

    # Combine the data into a single dataframe
    dfy = pd.DataFrame({"fx": fx, "gx": gx, "y": target})

    # Separate data into signal and background
    dfy_sb = dfy.groupby("y")

    # Set signal/background dataframes
    df0 = dfy_sb.get_group(0)
    df1 = dfy_sb.get_group(1)

    # grab the fx and gx values for those sig/bkg pairs
    fx0 = df0["fx"].values
    fx1 = df1["fx"].values
    gx0 = df0["gx"].values
    gx1 = df1["gx"].values

    # sig/bkg might be different sizes so trim the longer of the two to the min size
    max_size = min(len(fx0), len(fx1))
    fx0, fx1, gx0, gx1 = fx0[:max_size], fx1[:max_size], gx0[:max_size], gx1[:max_size]

    # find differently ordered pairs
    dos = calc_do(fx0=fx0, fx1=fx1, gx0=gx0, gx1=gx1)
    ado_val = np.mean(dos)

    return ado_val