from datetime import timedelta, datetime

from frcm.datamodel.model import FireRiskPrediction, Location, WeatherData, Observations, Forecast
from frcm.data_harvesting.client import WeatherDataClient
import frcm.FRC_service.compute
from database.firestore import *

class FireRiskAPI:

    def __init__(self, client: WeatherDataClient):
        self.client = client
        self.timedelta_ok = timedelta(days=1)
        self.interpolate_distance = 720

    def compute(self, wd: WeatherData) -> FireRiskPrediction:
        return frcm.FRC_service.compute.compute(wd)
    
    def get_day_bounds(self, date):
        start_day = datetime(date.year, date.month, date.day)
        end_day = start_day + timedelta(days=1)
        return start_day, end_day

    def fetch_and_check_data(self, location, start_time, time_now):
        days_to_fetch = []
        current_day = start_time
        while current_day < time_now:
            days_to_fetch.append(current_day)
            current_day += timedelta(days=1)
        existing_data, missing_dates = self.check_existing_data(location, days_to_fetch)
        return days_to_fetch, existing_data, missing_dates

    def check_existing_data(self, location, days_to_fetch):
        start_day, _ = self.get_day_bounds(days_to_fetch[0])
        _, end_day = self.get_day_bounds(days_to_fetch[-1])
        all_db_data = get_date_weatherdata(location, start_day.strftime('%d-%m-%Y'), end_day.strftime('%d-%m-%Y'))
        all_db_data = all_db_data if all_db_data is not None else []
        data_by_date = {obs.data[0].timestamp.strftime('%d-%m-%Y'): obs for obs in all_db_data}
        
        existing_data = {}
        missing_dates = []
        for day in days_to_fetch:
            start_day, _ = self.get_day_bounds(day)
            formatted_date = start_day.strftime('%d-%m-%Y')
            db_data = data_by_date.get(formatted_date)
            if db_data and db_data.data:
                existing_data[day] = db_data
            else:
                missing_dates.append(day)
        return existing_data, missing_dates

    def fetch_missing_data(self, location, missing_dates, existing_data):
        fetched_data = {}
        for day in missing_dates:
            start_day, end_day = self.get_day_bounds(day)
            observations = self.client.fetch_observations(location, start=start_day, end=end_day)
            save_data_to_db(location, start_day.strftime('%d-%m-%Y'), observations.data, observations.source)
            existing_data[day] = observations

    def aggregate_observations(self, days_to_fetch, existing_data):
        all_observations = []
        combined_source = ""
        combined_location = None
        for day in days_to_fetch:
            if day in existing_data:
                combined_source = existing_data[day].source
                combined_location = existing_data[day].location
                all_observations.extend(existing_data[day].data)
        if not all_observations:
            raise Exception("No observation data available for processing.")
        return Observations(source=combined_source, location=combined_location, data=all_observations)

    def compute_previous_days(self, location: Location, delta: timedelta) -> FireRiskPrediction:
        time_now = datetime.now()
        start_time = time_now - delta
        days_to_fetch, existing_data, missing_dates = self.fetch_and_check_data(location, start_time, time_now)
        self.fetch_missing_data(location, missing_dates, existing_data)
        combined_observations = self.aggregate_observations(days_to_fetch, existing_data)
        # as normal 
        forecast = self.client.fetch_forecast(location, start_time, time_now)
        wd = WeatherData(created=time_now, observations=combined_observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction
    
    
    def compute_upcoming_days(self, location: Location, delta: timedelta) -> FireRiskPrediction: 
        time_now = datetime.now()
        end_time = time_now + delta
        observations = self.client.fetch_observations(location, start=time_now, end=end_time)
        # as normal
        forecast = self.client.fetch_forecast(location, time_now, end_time)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction

    def compute_specific_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
        time_now = datetime.now()
        observations = self.client.fetch_observations(location, start=start, end=time_now)
        days_to_fetch, existing_data, missing_dates = self.fetch_and_check_data(location, start, time_now)
        self.fetch_missing_data(location, missing_dates, existing_data)
        
        if start < time_now:
            observations = self.aggregate_observations(days_to_fetch, existing_data)

        # as normal
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


