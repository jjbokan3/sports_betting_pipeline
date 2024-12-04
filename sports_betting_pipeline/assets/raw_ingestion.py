from dagster import asset
import requests
from sports_betting_pipeline.config.constants import GET_SPORTS, GET_ODDS
import requests
import time
from pydantic import BaseModel, Field
from typing import List, Optional
from ..config.dlt_project.pipeline import run_dlt_pipeline

limit_sports = [
    "americanfootball_ncaaf",
    "americanfootball_nfl",
    "baseball_mlb",
    "basketball_nba",
    "basketball_ncaab",
]


@asset(required_resource_keys={"aws_secret_manager"})
def available_sports(context) -> list:
    """
    Fetch sports data from an external API and return as a dictionary.
    """
    if limit_sports:
        return limit_sports

    try:
        # Fetch the API key from the secret manager
        get_secret = context.resources.aws_secret_manager
        secret = get_secret("the_odds")
        api_key = secret.get("the_odds_api_key")

        if not api_key:
            raise ValueError("API key not found in secrets.")

        # Make the API request
        context.log.info(f"Fetching data from API: {GET_SPORTS}")
        response = requests.get(
            GET_SPORTS,
            headers={"accept": "application/json"},
            params={"apiKey": api_key, "all": "true"},
        )

        # Handle response errors
        response.raise_for_status()

        # Log and return the JSON data
        data = response.json()
        sports_keys = [sport["key"] for sport in data]
        print(sports_keys)
        context.log.info(f"Successfully fetched data: {len(data)} items.")
        return data

    except requests.RequestException as e:
        context.log.error(f"Failed to fetch data from API: {e}")
        raise

    except Exception as e:
        context.log.error(f"Unexpected error: {e}")
        raise


@asset(required_resource_keys={"aws_secret_manager"})
def sports_file(context, available_sports) -> list:
    results = []

    try:
        # Fetch the API key from the secret manager
        get_secret = context.resources.aws_secret_manager
        secret = get_secret("the_odds")
        api_key = secret.get("the_odds_api_key")

        if not api_key:
            raise ValueError("API key not found in secrets.")
    except Exception as e:
        context.log.error(f"Unexpected error: {e}")
        raise

    for sport in available_sports:
        result, current_time = (
            requests.get(
                GET_ODDS.format(sport),
                headers={"accept": "application/json"},
                params={
                    "regions": "us",
                    "markets": "h2h,spreads,totals",
                    "apiKey": api_key,
                },
            ).json(),
            time.time(),
        )
        result_with_sport = {"id": sport, "events": result}
        results.append(result_with_sport)
    return results


@asset()
def flattened_sports_file(context, sports_file) -> list[dict]:
    class Outcome(BaseModel):
        name: str
        price: float

    class Market(BaseModel):
        key: str
        outcomes: List[Outcome]

    class Bookmaker(BaseModel):
        title: str
        markets: List[Market]

    class Event(BaseModel):
        id: str
        home_team: str
        away_team: str
        bookmakers: List[Bookmaker]

    class Sport(BaseModel):
        id: str
        events: List[Event]

    sports = [Sport(**sport) for sport in sports_file]

    flattened_sports = []

    for sport in sports:
        for event in sport.events:
            for bookmaker in event.bookmakers:
                for market in bookmaker.markets:
                    for outcome in market.outcomes:
                        flattened_sports.append(
                            {
                                "sports_id": sport.id,
                                "event_id": event.id,
                                "home_team": event.home_team,
                                "away_team": event.away_team,
                                "bookmaker": bookmaker.title,
                                "market": market.key,
                                "outcome_team": outcome.name,
                                "outcome_price": outcome.price,
                            }
                        )

    print(len(flattened_sports))
    return flattened_sports


@asset()
def load_sports_file(context, flattened_sports_file) -> None:
    run_dlt_pipeline(flattened_sports_file)
