#!/usr/bin/env python3
import os
import csv
import json
from datetime import date, datetime, timedelta

import keyring
import myfitnesspal

MFP_START_DATE = date(2017, 1, 2)
UPDATE_RANGE = 2

os.chdir(os.path.dirname(os.path.realpath(__file__)))


def load_client(username):
    return myfitnesspal.Client(username)


def scrape_data(mfp, start_date=MFP_START_DATE, totals={}, entries={}):
    current_day = start_date
    while(current_day <= date.today()):
        print('Loading', current_day)
        data = mfp.get_date(current_day)
        day_str = current_day.isoformat()
        totals[day_str] = data.totals
        entries[day_str] = data.totals
        entries[day_str]['entries'] = {e.name:e.totals for e in data.entries}
        current_day += timedelta(days=1)
    return totals, entries


def save_data(totals, entries):
    with open('totals.json', 'w') as f:
        json.dump(totals, f, indent=4)
    with open('entries.json', 'w') as f:
        json.dump(entries, f, indent=7)


def load_totals():
    with open('totals.json', 'r') as f:
        return json.load(f)


def load_entries():
    with open('entries.json', 'r') as f:
        return json.load(f)


def run(all_dates=False):
    mfp = load_client(keyring.get_password('mfp', 'user'))

    if all_dates:
        updated_totals, updated_entries = scrape_data(mfp)
    else:
        today = date.today()
        from_date = today - timedelta(days=UPDATE_RANGE)
        totals = load_totals()
        entries = load_entries()
        updated_totals, updated_entries = scrape_data(mfp, from_date, 
                                                      totals, entries)

    save_data(updated_totals, updated_entries)


def main():
    run(all_dates=False)
    print('Done')


if __name__ == '__main__':
    main()
