from dagster import Definitions, load_assets_from_modules

from sports_betting_pipeline.assets import cleaning, raw_ingestion  # noqa: TID252

all_assets = load_assets_from_modules([cleaning, raw_ingestion])

defs = Definitions(
    assets=all_assets,
)
