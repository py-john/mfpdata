#!/usr/bin/env python3
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import date, timedelta

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))

with open('entries.json', 'r') as f:
    totals = json.load(f)

df = pd.DataFrame.from_dict(totals).T

df[['carbohydrates','protein']] *= 4
df['fat'] *= 9
df['macro_cals'] = df[['fat', 'protein', 'carbohydrates']].sum(axis=1)
df['cal_diff'] = df['calories'] - df['macro_cals']

entrydf = df[['calories', 'macro_cals', 'entries']].copy()

edict = {}
edictlists = {}
for day in entrydf['entries']:
    for k, v in day.items():
        k = ','.join(k.split(',')[:-1])
        edict[k] = v

for day in entrydf['entries']:
    for k, v in day.items():
        k = ','.join(k.split(',')[:-1])
        templist =  edictlists.get(k, [])
        templist.append(v)
        edictlists[k] = templist[:]

edict = {}
counts = {}
for date, day in entrydf['entries'].items():
    for k, v in day.items():
        k = ','.join(k.split(',')[:-1])
        tmplist =  counts.get(k, [])
        tmplist.append(date)
        counts[k] = tmplist
        edict[k] = v
        edict[k]['dates'] = tmplist
        edict[k]['occurences'] = len(tmplist)
