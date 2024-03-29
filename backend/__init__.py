# Step 3: create job settings with BaseJob subclasses
JobSettings = {
    'data': {
        'job_class': 'backend.load_data.LoadData',
        'job_type': 'LoadData',
        'job_schedule': '0 3 * * 2-6',
        'max_failures': 30,
        'max_consecutive_failures': 10,
        'expire_hours': 12,
        'batch_size': 10,
        'process_interval_in_seconds': 5
    },
    'digest': {
        'job_class': 'backend.market_digest.MarketDigest',
        'job_type': 'MarketDigest',
        'job_schedule': '30 3 * * 2-6'
    }
}


TEMP_DIR = '../MarketDaily_Temp'

CONN_STR_ENV_VAR = 'MarketDailyConnStr'