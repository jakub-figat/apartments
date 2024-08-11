from enum import StrEnum

from pydantic import BaseModel, Field


class ApartmentListing(BaseModel):
    title: str
    location: str
    price: str
    url: str


class ApartmentListingPage(BaseModel):
    url: str
    listings: list[ApartmentListing] = Field(default_factory=list)


class HTMLRequestResult(BaseModel):
    url: str
    final_url: str
    html: str


class ApartmentRawDetails(BaseModel):
    url: str
    title: str
    description: str | None
    location: str
    inital_price: str


class Locations(StrEnum):
    BRONOWICE = "Bronowice"
    KROWODRZA = "Krowodrza"
    PRADNIK_BIALY = "Prądnik Biały"
    PRADNIK_CZERWONY = "Prądnik Czerwony"
