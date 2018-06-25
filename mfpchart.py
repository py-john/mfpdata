#!/usr/bin/env python3
import os
import json

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))


def get_dataframes():
    """Return totals and weight dataframes from json files."""
    with open(f'{PACKAGE_DIR}/totals.json', 'r') as f:
        totals = pd.DataFrame(json.load(f)).T
    with open(f'{PACKAGE_DIR}/weight.json', 'r') as f:
        weight = pd.Series(json.load(f)).T
    totals.index = pd.to_datetime(totals.index)
    weight.index = pd.to_datetime(weight.index)
    set_calories(totals)
    return totals, weight


def set_calories(df):
    """Set macro columns to calorie values and percentage to whole numbers."""
    df[['carbohydrates', 'protein']] *= 4
    df['fat'] *= 9
    df['macro_cals'] = df[['fat', 'protein', 'carbohydrates']].sum(axis=1)

    df.loc[:, :] = df[df['macro_cals'] != 0]

    df['crb_pct'] = df['carbohydrates'] * 100 / df['macro_cals']
    df['pro_pct'] = df['protein'] * 100 / df['macro_cals']
    df['fat_pct'] = df['fat'] * 100 / df['macro_cals']


def get_averages(df):
    """Return rolling mean dfs for calories and macro percentages."""
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


def plot_data(percent, calories, weight):
    """Plot the rolling means for calories and macro percentages."""
    fig = plt.figure(figsize=(9, 7))

    ax1 = fig.add_subplot(311)
    ax1.plot(calories)
    ax2 = fig.add_subplot(312)
    ax2.plot(percent)
    ax3 = fig.add_subplot(313)
    ax3.plot(weight)

    months = mdates.MonthLocator()
    major_months = mdates.MonthLocator(interval=2)
    date_fmt = mdates.DateFormatter("%b '%y")

    for ax in (ax1, ax2, ax3):
        ax.xaxis.set_major_locator(major_months)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_formatter(date_fmt)
        ax.tick_params(axis='x', rotation=20)
        ax.set_xlim([pd.Timestamp(2017, 1, 1), 
                     calories.index[-1] + pd.Timedelta('2 days')])

    ax3.set_ylim([160, 200])

    ax1.set_title('Calories')
    ax2.set_title('Percentages')
    ax3.set_title('Weight')

    plt.tight_layout()
    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(['Carbs', 'Fat', 'Protein', 'Total'])
    ax2.legend(['Carbs', 'Fat', 'Protein'])
    plt.show()


def main():
    """Get the dataframe and plot the data."""
    totals, weight = get_dataframes()
    percent, calories = get_averages(totals)
    plot_data(percent, calories, weight)


if __name__ == '__main__':
    main()
