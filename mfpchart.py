#!/usr/bin/env python3
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))


def get_dataframe():
    with open(f'{PACKAGE_DIR}/totals.json', 'r') as f:
        df = pd.DataFrame.from_dict(json.load(f)).T
    df.index = pd.to_datetime(df.index)
    set_calories(df)
    return df


def set_calories(df):
    df[['carbohydrates','protein']] *= 4
    df['fat'] *= 9
    df['macro_cals'] = df[['fat', 'protein', 'carbohydrates']].sum(axis=1)

    df.loc[:, :] = df[df['macro_cals'] != 0]

    df['crb_pct'] = df['carbohydrates'] * 100 / df['macro_cals']
    df['pro_pct'] = df['protein'] * 100 / df['macro_cals']
    df['fat_pct'] = df['fat'] * 100 / df['macro_cals']


def get_averages(df):
    df['crb_pct_mean'] = df['crb_pct'].rolling(window=8, center=False).mean()
    df['pro_pct_mean'] = df['pro_pct'].rolling(window=8, center=False).mean()
    df['fat_pct_mean'] = df['fat_pct'].rolling(window=8, center=False).mean()

    df['crb_mean'] = df['carbohydrates'].rolling(window=8, center=False).mean()
    df['pro_mean'] = df['protein'].rolling(window=8, center=False).mean()
    df['fat_mean'] = df['fat'].rolling(window=8, center=False).mean()
    df['cal_mean'] = df['calories'].rolling(window=8, center=False).mean()

    rolling_pct = df[['crb_pct_mean', 'fat_pct_mean', 'pro_pct_mean']]
    rolling_cals = df[['crb_mean', 'fat_mean', 'pro_mean', 'cal_mean']]

    return rolling_pct, rolling_cals


def plot_data(rolling_pct, rolling_cals):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(rolling_cals)
    ax2 = fig.add_subplot(212)
    ax2.plot(rolling_pct)

    major_months = mdates.MonthLocator(interval=2)
    months = mdates.MonthLocator()
    date_fmt = mdates.DateFormatter("%b '%y")

    ax1.xaxis.set_major_locator(major_months)
    ax1.xaxis.set_minor_locator(months)
    ax1.xaxis.set_major_formatter(date_fmt)

    ax2.xaxis.set_major_locator(major_months)
    ax2.xaxis.set_minor_locator(months)
    ax2.xaxis.set_major_formatter(date_fmt)

    ax1.tick_params(axis='x', rotation=20)
    ax2.tick_params(axis='x', rotation=20)

    ax1.set_title('Calories')
    ax2.set_title('Percentages')

    plt.tight_layout()
    plt.show()


df = get_dataframe()
rolling_pct, rolling_cals = get_averages(df)
plot_data(rolling_pct, rolling_cals)
