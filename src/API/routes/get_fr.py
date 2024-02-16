from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import BaseModel, validator
from typing import Optional  # Import Optional

router = APIRouter()

# Define a Pydantic model for the response
class ErrorResponse(BaseModel):
    detail: str

def calculate_fr_request_dummy(start_date, end_date, longitude, latitude):
    # A call to logic will be made here with date_span and cordinates.
    # logic.method(date_span, kordinates)

    # Mottar en firerisk klasse objekt. 

    return start_date, end_date, longitude, latitude

@router.get("/calculate/firerisk/", responses={
    404: {"model": ErrorResponse, "description": "no jobs"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(start_date: Optional[str] = Query(None, description="This paramter is the date to search from"),
                       end_date: Optional[str] = Query(None, description="This paramter is the date to search to"),
                       longitude: Optional[float] = Query(None, description="This paramter is the date to search from"),
                       latitude: Optional[float] = Query(None, description="This paramter is the date to search from")):
    
    #define date_span
    # longitude
    # latitude
    # Using DD - Decimal degrees

    return calculate_fr_request_dummy(start_date, end_date, longitude, latitude)


#URL EXAMPLE: http://127.0.0.1:8000/api/v1/calculate/firerisk/?start_date=hei&end_date=Okei&longitude=8.2&latitude=9.2