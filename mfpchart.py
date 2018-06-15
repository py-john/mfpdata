#!/usr/bin/env python3
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(f'{PACKAGE_DIR}/totals.json', 'r') as f:
    df = pd.DataFrame.from_dict(json.load(f)).T

df[['carbohydrates','protein']] *= 4
df['fat'] *= 9
df['macro_cals'] = df[['fat', 'protein', 'carbohydrates']].sum(axis=1)
df['cal_diff'] = df['calories'] - df['macro_cals']

df = df[df['macro_cals'] != 0]

df['crb_pct'] = df['carbohydrates'] / df['macro_cals']
df['pro_pct'] = df['protein'] / df['macro_cals']
df['fat_pct'] = df['fat'] / df['macro_cals']

df['crb_pct_mean'] = df['crb_pct'].rolling(window=7, center=False).mean()
df['pro_pct_mean'] = df['pro_pct'].rolling(window=7, center=False).mean()
df['fat_pct_mean'] = df['fat_pct'].rolling(window=7, center=False).mean()
rolling_pct = df[['crb_pct_mean', 'pro_pct_mean', 'fat_pct_mean']]

df['crb_mean'] = df['carbohydrates'].rolling(window=7, center=False).mean()
df['pro_mean'] = df['protein'].rolling(window=7, center=False).mean()
df['fat_mean'] = df['fat'].rolling(window=7, center=False).mean()
df['cal_mean'] = df['macro_cals'].rolling(window=7, center=False).mean()
rolling_cals = df[['crb_mean', 'fat_mean','pro_mean', 'cal_mean']]

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(rolling_pct)
ax2 = fig.add_subplot(212)
ax2.plot(rolling_cals)

plt.show()

# f, ax = plt.subplots(2, sharex=True)
# f.suptitle('Sharing X axis')
# ax[0].plot(rolling_pct)
# ax[1].plot(rolling_cals)
# plt.show()
