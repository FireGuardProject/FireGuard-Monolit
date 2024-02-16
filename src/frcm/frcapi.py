import datetime

from frcm.datamodel.model import FireRiskPrediction, Location, WeatherData, Observations, Forecast
from frcm.data_harvesting.client import WeatherDataClient
import frcm.FRC_service.compute


class FireRiskAPI:

    def __init__(self, client: WeatherDataClient):
        self.client = client
        self.timedelta_ok = datetime.timedelta(days=1) # TODO: when during a day is observations updated? (12:00 and 06:00)
        # TODO (NOTE): Short term forecast updates every 3rd hour with long term forecast every 12th hour at 12:00 and 06:00
        self.interpolate_distance = 720

    def compute(self, wd: WeatherData) -> FireRiskPrediction:

        return frcm.FRC_service.compute.compute(wd)
    

        #API input
    def compute_now(self, location: Location, obs_delta: datetime.timedelta) -> FireRiskPrediction: 
        '''
        This calcultes the fire risk prediction for a selected start time to now.
        '''
        time_now = datetime.datetime.now()
        start_time = time_now - obs_delta

        # databasen check() 

        observations = self.client.fetch_observations(location, start=start_time, end=time_now) # data harvesting



        forecast = self.client.fetch_forecast(location) # data harvesting

        wd = WeatherData(created=time_now, observations=observations, forecast=forecast) # data harvesting (FRM) 

        prediction = self.compute(wd)  # FRC 

        return prediction 

    def compute_now_period(self, location: Location, obs_delta: datetime.timedelta, fct_delta: datetime.timedelta):
        pass

    def compute_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
        pass

    def compute_period_delta(self, location: Location, start: datetime, delta: datetime.timedelta) -> FireRiskPrediction:
        pass


