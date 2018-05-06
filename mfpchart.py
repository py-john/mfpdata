#!/usr/bin/env python3

# from pprint import pprint
import os
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

today = totals[date.today().isoformat()]
if not today:
    today = totals[(date.today()-timedelta(days=1)).isoformat()]
t_c = today['carbohydrates'] * 4
t_p = today['protein'] * 4
t_f = today['fat'] * 9
t_cals = t_c + t_p + t_f
t_c_total = t_c/t_cals
t_p_total = t_p/t_cals
t_f_total = t_f/t_cals

### Matplotlib
fig = plt.figure(figsize=(10,6))
ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((2, 2), (0, 1), rowspan=1, colspan=1)
ax3 = plt.subplot2grid((2, 2), (1, 0), rowspan=1, colspan=2)

## stack plot - plot1
ax1.stackplot(dates, f_totals, p_totals, c_totals, colors=[red, green, blue])

ax1.plot([],[], color=blue, label="carbs", linewidth=8)
ax1.plot([],[], color=green, label="pro", linewidth=8)
ax1.plot([],[], color=red, label="fat", linewidth=8)
ax1.axes.set_ylim([0, 1])
ax1.axes.set_xlim([dates[0], dates[-1]])

ax1.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(45)

## pie chart - plot2
macros = [t_c_total, t_f_total, t_p_total]
labels = ['Carbs', 'Fat', 'Protein']
colors = [blue, red, green]

ax2.pie(macros,
        labels=labels,
        colors=colors,
        startangle=90,
        shadow=True,
        autopct='%1.1f%%')

ax2.axis('equal')

## line graph - plot3
ax3.set_title("Macro Data")
ax3.set_xlabel("Date")
ax3.set_ylabel("Amount (g)")
ax3.xaxis.label.set_color(blue)
ax3.yaxis.label.set_color(blue)
ax3.set_yticks([x for x in range(0,660,50)])

ax3.plot(dates, fatmean, label="Fat mean", color=red)
ax3.plot(dates, carbsmean, label="Carbs mean", color=blue)
ax3.plot(dates, promean, label="Protein mean", color=green)
# ax3.fill_between(dates, fatmean, 0, alpha=0.5, color=red)
# ax3.fill_between(dates, carbsmean, 0, alpha=0.5, color=blue)
# ax3.fill_between(dates, promean, 0, alpha=0.5, color=green)

for label in ax3.xaxis.get_ticklabels():
    label.set_rotation(45)
ax3.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
ax3.axes.set_xlim([dates[avg_frame-1], dates[-1]])


plt.subplots_adjust(left=0.08, bottom=0.16, right=0.83, top=0.95, wspace=0.50, hspace=.35)

plt.show()

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
