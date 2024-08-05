from batch_job.base_job import BaseJob
from datetime import datetime
import pandas as pd
import requests


def get_raw_data():
    endpoint = 'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=9999&offset=0&download=true'
    basic_headers = { 'User-Agent': 'LoadDataJob' }
    response = requests.get(endpoint, headers=basic_headers, timeout=5)
    response.raise_for_status()
    return response.json()


# Step 1: subclass the BaseJob
class LoadData(BaseJob):
    # Step 2: override either post_loop (single or limited tasks) or load_items + process_item (many tasks in batch)  
    def post_loop(self, run_date: datetime):
        df = pd.DataFrame(get_raw_data['data']['rows'])
        df.set_index('symbol', inplace=True)
        df.drop(columns=['url'], inplace=True)
        df['lastsale'] = df['lastsale'].apply(lambda x: float(str(x).replace('$', '')) if x else 0.0)
        df['netchange'] = df['netchange'].apply(lambda x: float(x) if x else 0.0)
        df['pctchange'] = df['pctchange'].apply(lambda x: float(str(x).replace('%', '')) if x else 0.0)
        df['marketCap'] = df['marketCap'].apply(lambda x: float(x) if x else 0.0)
        df['volume'] = df['volume'].apply(lambda x: int(x) if x else 0)
        self.job_data.upload_file('screener', 'screener_raw_{0}.pkl'.format(run_date.strftime('%Y-%m-%d')), lambda x: df.to_pickle(x) == None)

    # Step 3: optionally override get_expected_data and/or get_not_expected for dependency check
