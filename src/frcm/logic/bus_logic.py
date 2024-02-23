from datetime import timedelta, datetime

from frcm.datamodel.model import FireRiskPrediction, Location, WeatherData, Observations, Forecast
from frcm.data_harvesting.client import WeatherDataClient
import frcm.FRC_service.compute


class FireRiskAPI:

    def __init__(self, client: WeatherDataClient):
        self.client = client
        self.timedelta_ok = timedelta(days=1) # TODO: when during a day is observations updated? (12:00 and 06:00)
        # TODO (NOTE): Short term forecast updates every 3rd hour with long term forecast every 12th hour at 12:00 and 06:00
        self.interpolate_distance = 720

    def compute(self, wd: WeatherData) -> FireRiskPrediction:
        return frcm.FRC_service.compute.compute(wd)
    

    def compute_now_delta(self, location: Location, obs_delta: timedelta) -> FireRiskPrediction: 
        time_now = datetime.now()
        start_time = time_now - obs_delta
        observations = self.client.fetch_observations(location, start=start_time, end=time_now)
        forecast = self.client.fetch_forecast(location)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction 


    def compute_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
        observations = self.client.fetch_observations(location, start=start, end=end)
        forecast = self.client.fetch_forecast(location)
        wd = WeatherData(created=end, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction 


    def compute_period_delta(self, location: Location, start: datetime, delta: timedelta) -> FireRiskPrediction:
        end = start + delta
        observations = self.client.fetch_observations(location, start=start, end=end)
        forecast = self.client.fetch_forecast(location)
        wd = WeatherData(created=end, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction


