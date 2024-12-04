from dagster import Definitions, load_assets_from_modules

from sports_betting_pipeline.assets import cleaning, raw_ingestion  # noqa: TID252
from sports_betting_pipeline.resources.aws_resources import aws_secret_manager_resource

all_assets = load_assets_from_modules([cleaning, raw_ingestion])
all_resources = {"aws_secret_manager": aws_secret_manager_resource}

defs = Definitions(assets=all_assets, resources=all_resources)
