from batch_job.base_job import BaseJob
from datetime import datetime
import pandas as pd


class MarketDigest(BaseJob):
    def load_items(self, last_processed: str) -> (bool, list):
        return super().load_items(last_processed)
    
    def process_item(self, work_item) -> bool:
        return super().process_item(work_item)
    
    def post_loop(self, run_date: datetime):
        return super().post_loop(run_date)
