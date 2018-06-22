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


def plot_data(percent, cals):
    fig = plt.figure(figsize=(9, 7))

    ax1 = fig.add_subplot(211)
    ax1.plot(cals)
    ax2 = fig.add_subplot(212)
    ax2.plot(percent)

    months = mdates.MonthLocator()
    major_months = mdates.MonthLocator(interval=2)
    date_fmt = mdates.DateFormatter("%b '%y")

    for ax in (ax1, ax2):
        ax.xaxis.set_major_locator(major_months)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_formatter(date_fmt)
        ax.tick_params(axis='x', rotation=20)

    ax1.set_title('Calories')
    ax2.set_title('Percentages')

    plt.tight_layout()
    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(['Carbs', 'Fat', 'Protein', 'Total'])
    ax2.legend(['Carbs', 'Fat', 'Protein'])
    plt.show()


def main():
    df = get_dataframe()
    percent, calories = get_averages(df)
    plot_data(percent, calories)


if __name__ == '__main__':
    main()
