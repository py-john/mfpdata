#!/usr/bin/env python3
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(f'{PACKAGE_DIR}/totals.json', 'r') as f:
    totals = json.load(f)

df = pd.DataFrame.from_dict(totals).T

df[['carbohydrates','protein']] *= 4
df['fat'] *= 9
df['macro_cals'] = df[['fat', 'protein', 'carbohydrates']].sum(axis=1)
df['cal_diff'] = df['calories'] - df['macro_cals']

df = df[df['macro_cals'] != 0]

df['crb_pct'] = df['carbohydrates'] / df['macro_cals']
df['pro_pct'] = df['protein'] / df['macro_cals']
df['fat_pct'] = df['fat'] / df['macro_cals']

edict = {}
for day in df['entries']:
    for food_item, macros in day.items():
        name = ','.join(food_item.split(',')[:-1])
        templist = edict.get(name, [])
        templist.append(macros)
        edict[name] = templist[:]

