import json
from datetime import datetime
import time
import numpy as np
import pandas as pd


def write_influxdb(records: list, batch_limit: int = 10000, data_type: str = 'float'):
    # script-engine function, defined here for reference only
    pass


def read_data(path):
    with open(path, 'r') as f:
        data = json.load(f)

    return data.copy()


def inspect_data(data):
    print(f'number of objects: {len(data)}')

    for obj in data:
        print()
        for k in obj.keys():
            if type(obj[k][:3]) == list:
                print(f'{k}:{obj[k][:3]}')
            else:
                print(f'{k}:{obj[k][:]}')

    for obj in data:
        print()
        print(f'keys: {list(obj.keys())}')
        print(f'tag_name: {obj["tag_name"]}')
        print(f'number of values: {len(obj["values"])}')
        print(f'number of timestamps: {len(obj["timestamp"])}')


def get_start_timestamp():
    return np.datetime64(datetime.utcnow(), 'ns') - np.timedelta64(1, 'h')


def update_timestamps(start, n):
    return [start.astype(np.int64) + i for i in range(n)]


def update_data(data):
    new_data = []
    start_ts = get_start_timestamp()
    n = 0

    for obj in data.copy():
        n = len(obj['timestamp'])
        obj['timestamp'] = update_timestamps(start_ts, n)
        new_data.append(obj)

    new_data.append(
        {
            'tag_name': 'VIB_TEST.WF.EVTID',
            'timestamp': [start_ts.astype(np.int64)] * n,
            'values': list(map(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%M:%S'), [start_ts]*n))
        }
    )

    new_data.append(
        {
            'tag_name': 'VIB_TEST.WF.EVT_CHG_ID',
            'timestamp': [start_ts.astype(np.int64)],
            'values': list(map(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%M:%S'), [start_ts]))
        }
    )

    return new_data


def main():
    no_of_tests = 3
    while no_of_tests > 0:
        print(f'#### START ######')
        start = time.time()

        data = read_data('data.json')
        inspect_data(data)
        # sim_data = update_data(data)
        # inspect_data(sim_data)

        # write_influxdb(records=sim_data, batch_limit=1000, data_type='float')

        no_of_tests -= 1

        end = time.time()
        print(f'#### END ######')
        print(f'Cycle time: {end - start} sec')

        time.sleep(10)


if __name__ == '__main__':
    main()

