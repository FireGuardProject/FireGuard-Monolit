from datetime import timedelta, datetime
from fastapi import FastAPI
import requests
import json

from frcm.datamodel.model import FireRiskPrediction, Location, WeatherData, Observations, Forecast
from frcm.data_harvesting.client import WeatherDataClient
import frcm.FRC_service.compute
from frcm.data_harvesting.client_met import METClient
from frcm.data_harvesting.extractor_met import METExtractor


class FireRiskAPI:

    def __init__(self, client: WeatherDataClient):
        self.client = client
        self.timedelta_ok = timedelta(days=1) # TODO: when during a day is observations updated? (12:00 and 06:00)
        # TODO (NOTE): Short term forecast updates every 3rd hour with long term forecast every 12th hour at 12:00 and 06:00
        self.interpolate_distance = 720

    def compute(self, wd: WeatherData) -> FireRiskPrediction:
        return frcm.FRC_service.compute.compute(wd)
    

    def compute_previous_days(self, location: Location, delta: timedelta) -> FireRiskPrediction: 
        time_now = datetime.now()
        start_time = time_now - delta

        # request to: dataharvesting microservice
        observations = self.client.fetch_observations(location, start=start_time, end=time_now)
        forecast = self.client.fetch_forecast(location, start_time, time_now)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction 

    def compute_upcoming_days(self, location: Location, delta: timedelta) -> FireRiskPrediction: 
        time_now = datetime.now()
        end_time = time_now + delta
        observations = self.client.fetch_observations(location, start=time_now, end=end_time)
        forecast = self.client.fetch_forecast(location, time_now, end_time)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction

    def compute_specific_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
        time_now = datetime.now()
        observations = self.client.fetch_observations(location, start=start, end=end)
        forecast = self.client.fetch_forecast(location, start, end)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction 

    def compute_after_start_date(self, location: Location, start: datetime, delta: timedelta) -> FireRiskPrediction:
        time_now = datetime.now()
        end = start + delta
        observations = self.client.fetch_observations(location, start=start, end=end)
        forecast = self.client.fetch_forecast(location, start, end)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction

    def compute_before_end_date(self, location: Location, end: datetime, delta: timedelta) -> FireRiskPrediction:
        time_now = datetime.now()
        start = end - delta
        observations = self.client.fetch_observations(location, start=start, end=end)
        forecast = self.client.fetch_forecast(location, start, end)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction
    

met_extractor = METExtractor()
# TODO: maybe embed extractor into client
met_client = METClient(extractor=met_extractor)
frc = FireRiskAPI(client=met_client)

app = FastAPI()
@app.get("/api/v1/fireriskPreviousDays")
def fire_risk_previous_days(days: int, longitude: float, latitude: float):
    time_delta = timedelta(days=days)
    location1 = Location(longitude=float(longitude), latitude=float(latitude))
    result = frc.compute_previous_days(location=location1, delta=time_delta)
    return result