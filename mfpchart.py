#!/usr/bin/env python3

# from pprint import pprint
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from mfpload import load_data
from datetime import date, timedelta

red = "#ff7373"
green = "#1fd084"
blue = "#3399ff"

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))

totals = load_data()

df = pd.DataFrame.from_dict(totals).T
df.index = pd.to_datetime(df.index, infer_datetime_format=True)
cals = df.copy()

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

food_items = pd.DataFrame(edict).T
food_items.index = food_items.index.str.capitalize()

food_items['cal_diff'] = food_items['calories'] - (food_items['carbohydrates']*4 + food_items['protein']*4 + food_items['fat']*9)
food_items['pct_diff'] = abs(food_items['cal_diff']/food_items['calories'])

del food_items['sugar']
# del food_items['fiber']

cols = ['dates', 'occurences', 'fiber','carbohydrates', 'protein', 'fat', 'calories']

# cols = ['pct_diff', 'cal_diff', 'fiber','carbohydrates', 'protein', 'fat', 'calories']
