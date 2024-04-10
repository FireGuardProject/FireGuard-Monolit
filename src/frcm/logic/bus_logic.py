from datetime import timedelta, datetime
from frcm.datamodel.model import FireRiskPrediction, Location, WeatherData, Observations, Forecast
from frcm.data_harvesting.client import WeatherDataClient
import frcm.FRC_service.compute
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#class FireRiskAPI:
#
#    def __init__(self, client: WeatherDataClient):
#        self.client = client
#        self.timedelta_ok = timedelta(days=1) # TODO: when during a day is observations updated? (12:00 and 06:00)
#        # TODO (NOTE): Short term forecast updates every 3rd hour with long term forecast every 12th hour at 12:00 and 06:00
#        self.interpolate_distance = 720
#



app = FastAPI()

def compute( wd: WeatherData) -> FireRiskPrediction:
    # REQUEST TO: FRCM service
    return frcm.FRC_service.compute.compute(wd)


@app.get("/api/v1/fireriskPreviousDays")
async def calculate_firerisk(days: int, longitude: float, latitude: float):

    delta = timedelta(days=days)

    try:
        # Here you adapt the given compute_previous_days logic to work in this context
        time_now = datetime.now()
        start_time = time_now - delta

        observations = WeatherDataClient.fetch_observations(Location(latitude=latitude, longitude=longitude), start=start_time, end=time_now)
        forecast = WeatherDataClient.fetch_forecast(Location(latitude=latitude, longitude=longitude), start_time, time_now)

        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)

        prediction = compute(wd)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e} I tried at least bitch!,latiitude: {latitude},longnitude: {longitude}, days: {days}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2000)



#@app.get("/v1/fireriskPreviousDays")
#async def calculate_firerisk(days: int, longitude: float, latitude: float):
#    time_now = datetime.now()
#    start_time = time_now - delta
#
#    # REQUEST TO: DataHarvestingClient
#    observations = WeatherDataClient.fetch_observations(location, start=start_time, end=time_now)
#    forecast = WeatherDataClient.fetch_forecast(location, start_time, time_now)
#
#    # formating of data: 
#    wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
#
#    # REQUEST TO: FRCM service
#    prediction = compute(wd)
#    return prediction 
#



#    def compute_upcoming_days(self, location: Location, delta: timedelta) -> FireRiskPrediction: 
#        time_now = datetime.now()
#        end_time = time_now + delta
#        observations = self.client.fetch_observations(location, start=time_now, end=end_time)
#        forecast = self.client.fetch_forecast(location, time_now, end_time)
#        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
#        prediction = self.compute(wd)
#        return prediction
#
#    def compute_specific_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
#        time_now = datetime.now()
#        observations = self.client.fetch_observations(location, start=start, end=end)
#        forecast = self.client.fetch_forecast(location, start, end)
#        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
#        prediction = self.compute(wd)
#        return prediction 
#
#    def compute_after_start_date(self, location: Location, start: datetime, delta: timedelta) -> FireRiskPrediction:
#        time_now = datetime.now()
#        end = start + delta
#        observations = self.client.fetch_observations(location, start=start, end=end)
#        forecast = self.client.fetch_forecast(location, start, end)
#        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
#        prediction = self.compute(wd)
#        return prediction
#
#    def compute_before_end_date(self, location: Location, end: datetime, delta: timedelta) -> FireRiskPrediction:
#        time_now = datetime.now()
#        start = end - delta
#        observations = self.client.fetch_observations(location, start=start, end=end)
#        forecast = self.client.fetch_forecast(location, start, end)
#        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
#        prediction = self.compute(wd)
#        return prediction
#