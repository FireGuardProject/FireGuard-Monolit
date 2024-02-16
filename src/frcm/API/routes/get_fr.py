from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import BaseModel, validator
from typing import Optional  # Import Optional
from logikk import endelig_funksjon
import datetime

router = APIRouter()

# Define a Pydantic model for the response
class ErrorResponse(BaseModel):
    detail: str

def calculate_fr_request(start_date, end_date, longitude, latitude):
    # Her skal en direkte kall direkte til en calculate metode i logic.
    #
    #
    return endelig_funksjon(start_date, end_date, longitude, latitude)

    return start_date, end_date, longitude, latitude

def check_date(date_first, date_last):
    if date_first >= date_last:
        raise HTTPException(status_code=400, detail="The end date must be after the start date.")


@router.get("/calculate/firerisk/", responses={
    404: {"model": ErrorResponse, "description": "firerisk no found"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(start_date: Optional[datetime.datetime] = Query(None, description="This paramter is the date to search from"),
                       end_date: Optional[datetime.datetime] = Query(None, description="This paramter is the date to search to"),
                       longitude: Optional[float] = Query(None, description="This paramter is the date to search from"),
                       latitude: Optional[float] = Query(None, description="This paramter is the date to search from")):
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
   
    check_date(start_date, end_date)

    return calculate_fr_request(start_date, end_date, longitude, latitude)


# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/calculate/firerisk/?start_date=2024-02-25&end_date=2024-03-25&longitude=60.39299&latitude=5.32415