import asyncio
from typing import Iterator

from httpx import AsyncClient

from model import HTMLRequestResult

OLX_APARTMENT_LIST_URL = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Bfilter_enum_furniture%5D%5B0%5D=yes&page={}"
OTODOM_APARTMENT_URL = ""
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


async def request_olx_list_in_parallel(page_numbers: list[int]) -> list[HTMLRequestResult]:
    url_iterator = (OLX_APARTMENT_LIST_URL.format(page_number) for page_number in page_numbers)
    results = []

    await asyncio.gather(*(_request_html_from_olx(url_iterator, results) for _ in range(3)))
    return results


async def request_olx_apartment_pages_in_parallel(apartment_urls: list[str]) -> list[HTMLRequestResult]:
    url_iterator = iter(apartment_urls)
    results = []

    await asyncio.gather(*(_request_html_from_olx(url_iterator, results) for _ in range(10)))
    return results


async def _request_html_from_olx(url_iterator: Iterator[str], results: list[HTMLRequestResult]) -> None:
    async with AsyncClient(headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=600) as client:
        while (url := next(url_iterator, None)) is not None:
            response = await client.get(url)
            response.raise_for_status()

            results.append(HTMLRequestResult(html=response.text, url=url, final_url=str(response.url)))
