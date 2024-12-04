from urllib.parse import urljoin

THE_ODDS_ENDPOINT = "https://api.the-odds-api.com/v4/sports"
GET_SPORTS = THE_ODDS_ENDPOINT
GET_ODDS = THE_ODDS_ENDPOINT + "/{}/odds"
GET_SCORES = THE_ODDS_ENDPOINT + "/{}/scores"
GET_EVENTS = THE_ODDS_ENDPOINT + "/{}/events"
GET_EVENT_ODDS = GET_EVENTS + "/{}/odds"
GET_HISTORICAL_EVENTS = GET_EVENTS
GET_HISTORICAL_ODDS = GET_ODDS
