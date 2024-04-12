from fastapi import APIRouter, Query, Path, HTTPException, Depends
from pydantic import BaseModel, validator
from typing import Optional  # Import Optional
from datetime import datetime, timedelta
from frcm.logic.bus_logic import FireRiskAPI
from frcm.datamodel.model import Location
from frcm.data_harvesting.client_met import METClient
from frcm.data_harvesting.extractor_met import METExtractor
from frcm.API.bearer_token.token import get_current_user

router = APIRouter()
met_extractor = METExtractor()
# TODO: maybe embed extractor into client
met_client = METClient(extractor=met_extractor)
frc = FireRiskAPI(client=met_client)

# Define a Pydantic model for the response
class ErrorResponse(BaseModel):
    detail: str


def calculate_firerisk(end_date, days, longitude, latitude):
    delta = timedelta(days=days)
    location = Location(longitude=longitude, latitude=latitude)
    end = datetime.fromisoformat(end_date)
    FireRiskPrediction = frc.compute_before_end_date(location, end, delta)
    return FireRiskPrediction


@router.get("/v1/fireriskBeforeEndDate", responses={
    404: {"model": ErrorResponse, "description": "firerisk not found"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(end_date: Optional[str] = Query(None, description="This parameter is the date to search to"),
                       days: Optional[int] = Query(None, description="This parameter is the time delta"),
                       longitude: Optional[float] = Query(None, description="This parameter is the longitude for the location"),
                       latitude: Optional[float] = Query(None, description="This parameter is the latitude for the location")):

    return calculate_firerisk(end_date, days, longitude, latitude)


@router.get("/v2/fireriskBeforeEndDate")
async def get_firerisk_with_authorization(
        end_date: Optional[str] = Query(None, description="Date to search to"),
        days: Optional[int] = Query(None, description="Time delta"),
        longitude: Optional[float] = Query(None, description="Longitude"),
        latitude: Optional[float] = Query(None, description="Latitude"),
        current_user: str = Depends(get_current_user)):

    return calculate_firerisk(end_date, days, longitude, latitude)

# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/fireriskBeforeEndDate/?start_date=2024-03-10&days=3&longitude=60.39299&latitude=5.32415