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


def calculate_fr_period(start_date, end_date, longitude, latitude):
    location = Location(longitude=longitude, latitude=latitude)
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    FireRiskPrediction = frc.compute_period(location, start, end)
    return FireRiskPrediction


def check_date(date_first, date_last):
    if date_first >= date_last:
        raise HTTPException(status_code=400, detail="The end date must be after the start date.")


@router.get("/calculate/firerisk/period", responses={
    404: {"model": ErrorResponse, "description": "firerisk no found"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(start_date: Optional[str] = Query(None, description="This parameter is the date to search from"),
                       end_date: Optional[str] = Query(None, description="This parameter is the date to search to"),
                       longitude: Optional[float] = Query(None, description="This parameter is the date to search from"),
                       latitude: Optional[float] = Query(None, description="This parameter is the date to search from")):
    """
        This endpoint taks inn four parameters and returns a list of firerisks.

        Args:
        - start_date = a date in the form of year-month-day
        - end_date = a date in the form of year-month-day. The date has to be after the start_date in order for the function to work.
        - longitude = a float value of longitude. like 86.89200
        - latitude = a float value of latitude. like 35.28301
    
        Output:
        - list of firerisks.

        Example  URL:
        http://127.0.0.1:8000/api/v1/calculate/firerisk/?start_date=2024-02-25&end_date=2024-03-25&longitude=60.39299&latitude=5.32415
    """
   
    # check_date(start_date, end_date)

    return calculate_fr_period(start_date, end_date, longitude, latitude)


# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/calculate/firerisk/?start_date=2024-02-25&end_date=2024-03-25&longitude=60.39299&latitude=5.32415