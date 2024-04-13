import argparse
import io

import pandas as pd
import requests

def chunk_timeframe(start_date, end_date):
    delta = start_date + pd.Timedelta(days=1)
    if (delta > end_date):
        calculate_averages(start_date, end_date)
        return
    else:
        calculate_averages(start_date, delta)
        chunk_timeframe(delta + pd.Timedelta(seconds=1), end_date)

def calculate_averages(start_date, end_date):
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    payload = {'begin': start_date.strftime(time_format), 'end': end_date.strftime(time_format)}
    res = requests.get('https://tsserv.tinkermode.dev/data', params=payload)
    ts = pd.read_fwf(io.StringIO(res.text), index_col=0, parse_dates=True,
     date_format=time_format, header=None)
    ts1 = ts.resample('60Min').mean()
    for row in ts1.itertuples():
        print(row.Index.strftime(time_format), f'{row._1:.4f}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("start_date")
    parser.add_argument("end_date")
    args = parser.parse_args()
    start_date = pd.Timestamp(args.start_date).replace(minute=0, second=0)
    end_date = pd.Timestamp(args.end_date).replace(minute=59, second=59)
    chunk_timeframe(start_date, end_date)

main()