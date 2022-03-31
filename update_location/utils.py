import os

import requests
from dotenv import load_dotenv
from pycountry import countries

load_dotenv()

main_dict = dict()


def get_country_code(country):
    country_code = countries.get(name=country)
    return country_code.alpha_2 if country_code else ''


def get_locations(location=None, country='all'):
    if main_dict.get((country, location), False):
        return main_dict.get((country, location))
    if country == 'all':
        response = requests.get(
            f"{os.environ.get('BASE_GEONAMES_URL')}?q={location}&username={os.environ.get('GEONAMES_USER')}")
    else:
        response = requests.get(
            f"{os.environ.get('BASE_GEONAMES_URL')}?q={location}&country={get_country_code(country)}&username={os.environ.get('GEONAMES_USER')}")
    update_main_dict(response_data=response.json(), location=location, country=country)

    return main_dict.get((country, location))


def parse_location(response_data):
    location_data = []
    for data in response_data['geonames']:
        new_location = dict()
        new_location['toponymName'] = data.get('toponymName', '')
        new_location['name'] = data.get('name', '')
        new_location['lng'] = data.get('lng', '')
        new_location['lat'] = data.get('lat', '')
        new_location['countryCode'] = data.get('countryCode', '')
        new_location['countryName'] = data.get('countryName', '')
        new_location['countryId'] = data.get('countryId', '')
        new_location['population'] = data.get('population', 0)
        location_data.append(new_location)

    return location_data


def update_main_dict(response_data, location, country):
    if not main_dict.get((country, location), False):
        location_data = parse_location(response_data)
        main_dict[(country, location)] = location_data
