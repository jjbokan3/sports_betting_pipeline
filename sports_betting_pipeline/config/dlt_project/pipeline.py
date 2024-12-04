import dlt
from typing import List, Dict


@dlt.resource(name="sports_data")
def sports_data(data: List[Dict]):
    # Directly yield the records
    for record in data:
        yield record


pipeline = dlt.pipeline(
    pipeline_name="sports_betting_pipeline",
    destination="bigquery",
    dataset_name="raw_data",
)


def run_dlt_pipeline(data: List[Dict]):
    # Pass data to the pipeline
    load_info = pipeline.run(sports_data(data))
    print(f"Loaded {load_info.loads_total} records into BigQuery.")
