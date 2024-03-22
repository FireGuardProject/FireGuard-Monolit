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


def calculate_firerisk(days, longitude, latitude):
    delta = timedelta(days=days)
    location = Location(longitude=longitude, latitude=latitude)
    FireRiskPrediction = frc.compute_upcoming_days(location, delta)
    return FireRiskPrediction


@router.get("/fireriskUpcomingDays", responses={
    404: {"model": ErrorResponse, "description": "firerisk not found"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(days: Optional[int] = Query(None, description="This parameter is the time delta"),
                       longitude: Optional[float] = Query(None, description="This parameter is the longitude for the location"),
                       latitude: Optional[float] = Query(None, description="This parameter is the latitude for the location")):

    return calculate_firerisk(days, longitude, latitude)


# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/fireriskUpcomingDays/?days=3&longitude=60.39299&latitude=5.32415