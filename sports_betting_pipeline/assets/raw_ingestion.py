from dagster import asset

@asset
def basic_ingestion() -> None:
    return {'basic': 'json'}