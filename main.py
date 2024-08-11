import asyncio
import re

from files import save_apartments_to_txt_file
from model import Locations
from network import request_olx_list_in_parallel, request_olx_apartment_pages_in_parallel
from parser import parse_olx_listing_page, parse_apartment
from settings import settings

ac_pattern = re.compile('|'.join([
    r'air\s*conditioning',
    r'air\s*conditioner',
    r'ac\s*unit',
    r'klimatyzacja',
    r'klimatyzacji',
    r'klimatyzację',
    r'klimatyzacją',
    r'klimatyzacjo',
    r'klimatyzator',
    r'klimatyzatora',
    r'klimatyzatorze',
    r'klimatyzatorowi',
    r'klimatyzatorem',
    r'klimatyzatorze',
    r'klimatyzatorze',
    r'klima',
    r'klimie',
    r'chłodzenie\s*powietrza',
]), re.IGNORECASE)


async def main():
    olx_htmls = await request_olx_list_in_parallel(page_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    pages = [parse_olx_listing_page(html) for html in olx_htmls]
    url_to_location_dict = {listing.url: listing.location for page in pages for listing in page.listings}

    apartment_htmls = await request_olx_apartment_pages_in_parallel([listing.url for page in pages for listing in page.listings])
    apartments = [parse_apartment(html.html, html.final_url, url_to_location_dict[html.url]) for html in apartment_htmls]
    apartments = [apartment for apartment in apartments if apartment.location in (
        Locations.BRONOWICE.value,
        Locations.PRADNIK_BIALY.value,
        Locations.PRADNIK_CZERWONY.value,
        Locations.KROWODRZA.value
    )
                  ]

    if settings.AIR_CONDITIONING_SEARCH:
        apartments = [apartment for apartment in apartments if ac_pattern.search(apartment.description)]

    save_apartments_to_txt_file(apartments)

if __name__ == '__main__':
    asyncio.run(main())
