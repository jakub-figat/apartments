from model import ApartmentRawDetails
import random


def save_apartments_to_txt_file(apartments: list[ApartmentRawDetails]) -> None:
    with open(f"apartments-{random.randint(1, 1_000_000)}.txt", "w") as file:
        file.write("\n".join(
            f"{apartment.url} - {apartment.title} - {apartment.location} - {apartment.inital_price}"
            for apartment in apartments
        ))
