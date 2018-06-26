#!/usr/bin/env python3
import os
import json
from datetime import date, datetime, timedelta

import keyring
import myfitnesspal

MFP_START_DATE = date(2017, 1, 2)

os.chdir(os.path.dirname(os.path.realpath(__file__)))


def load_client(username):
    """Return mfp client for given username."""
    return myfitnesspal.Client(username)


def scrape_data(mfp, start_date=MFP_START_DATE, totals={}, weight={}):
    """Update and return totals dict starting from a given date.

    If no keyword args are given all the available data will be saved.
    totals has all the macro data, the 'entries' key is for the meal logs.
    """
    current_day = start_date
    while(current_day <= date.today()):
        print('Loading', current_day)
        data = mfp.get_date(current_day)
        day_str = current_day.isoformat()
        totals[day_str] = data.totals
        totals[day_str]['entries'] = {e.name: e.totals for e in data.entries}
        current_day += timedelta(days=1)
    new_weight = mfp.get_measurements('Weight', start_date)
    for w in reversed(new_weight):
        day_str = w.isoformat()
        weight[day_str] = new_weight[w]
    return totals, weight


def save_data(totals, weight):
    """Save totals and weight data to json."""
    with open('totals.json', 'w') as f:
        json.dump(totals, f, indent=4)
    with open('weight.json', 'w') as f:
        json.dump(weight, f, indent=4)


def load_data():
    """Return totals and weight json data."""
    with open('totals.json', 'r') as f:
        totals = json.load(f)
    with open('weight.json', 'r') as f:
        weight = json.load(f)
    return totals, weight


def run(all_dates=False):
    """Save data from mfp client for specific time frame."""
    mfp = load_client(keyring.get_password('mfp', 'user'))
    if all_dates:
        new_totals, new_weight = scrape_data(mfp)
    else:
        totals, weight = load_data()
        last_date = datetime.strptime(sorted(totals.keys())[-1],
                                      '%Y-%m-%d').date()
        from_date = last_date - timedelta(days=1)
        new_totals, new_weight = scrape_data(mfp, from_date, totals, weight)

    save_data(new_totals, new_weight)


def main():
    """Run the mfp scraper."""
    run(all_dates=False)
    print('Done')


if __name__ == '__main__':
    main()
