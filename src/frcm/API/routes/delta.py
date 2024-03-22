from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import BaseModel, validator
from typing import Optional  # Import Optional
from datetime import datetime, timedelta
from frcm.logic.bus_logic import FireRiskAPI
from frcm.datamodel.model import Location
from frcm.data_harvesting.client_met import METClient
from frcm.data_harvesting.extractor_met import METExtractor

router = APIRouter()
met_extractor = METExtractor()
# TODO: maybe embed extractor into client
met_client = METClient(extractor=met_extractor)
frc = FireRiskAPI(client=met_client)

# Define a Pydantic model for the response
class ErrorResponse(BaseModel):
    detail: str



def calculate_fr_period_delta(start_date, timedelta_days, longitude, latitude):
    obs_delta = timedelta(days=timedelta_days)
    location = Location(longitude=longitude, latitude=latitude)
    start = datetime.fromisoformat(start_date)
    FireRiskPrediction = frc.compute_period_delta(location, start, obs_delta)
    return FireRiskPrediction




@router.get("/calculate/firerisk/period/delta", responses={
    404: {"model": ErrorResponse, "description": "firerisk no found"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(start_date: Optional[str] = Query(None, description="This parameter is the date to search from"),
                       timedelta_days: Optional[int] = Query(None, description="This parameter is the time delta"),
                       longitude: Optional[float] = Query(None, description="This parameter is the date to search from"),
                       latitude: Optional[float] = Query(None, description="This parameter is the date to search from")):

    return calculate_fr_period_delta(start_date, timedelta_days, longitude=longitude, latitude=latitude)



# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/calculate/firerisk/period/delta?start_date=2024-03-10&timedelta_days=5&longitude=7.9956&latitude=58.14671