from model import ApartmentListingPage, ApartmentListing, HTMLRequestResult, ApartmentRawDetails
from bs4 import BeautifulSoup

from settings import settings


def parse_olx_listing_page(html_result: HTMLRequestResult) -> ApartmentListingPage:
    soup = BeautifulSoup(html_result.html, features="lxml", parser="lxml")
    listing_grid_container_div = soup.select_one("div.listing-grid-container")
    listings = []
    for listing in listing_grid_container_div.select("div[data-testid=l-card]"):
        url = listing.select_one('a').get('href')
        if "http" in url:
            if "otodom" in url and settings.IGNORE_OTODOM_REDIRECTS:
                continue
        else:
            url = f"https://olx.pl{url}"

        listings.append(ApartmentListing(
            title=listing.select_one("h6").text,
            price=listing.select_one("p[data-testid=ad-price]").text,
            location=_parse_location_from_olx_string(listing.select_one("p[data-testid=location-date]").text),
            url=url
        ))

    return ApartmentListingPage(url=html_result.final_url, listings=listings)


def parse_apartment(apartment_html: str, url: str, location: str) -> ApartmentRawDetails:
    soup = BeautifulSoup(apartment_html, features="lxml", parser="lxml")
    title = soup.select_one("div[data-testid=ad_title]>h4").text
    initial_price = soup.select_one("div[data-testid=ad-price-container]>h3").text
    description = description_div.text if (description_div := soup.select_one("div[data-testid=ad_description]")) is not None else None

    return ApartmentRawDetails(
        url=url,
        title=title,
        inital_price=initial_price,
        location=location,
        description=description
    )


def _parse_location_from_olx_string(location: str) -> str:
    left_side, *_ = location.split(" - ", maxsplit=1)
    return left_side.split(", ", maxsplit=1)[1]
