from django.contrib.gis.geos import Point
from geopy.geocoders import Yandex


def get_coordinates(address):
    yandex_geocoder = Yandex(user_agent='navalny.notifier', timeout=60)
    location = yandex_geocoder.geocode(address, exactly_one=True)
    return Point(x=location.latitude, y=location.longitude, srid=4326) \
        if location and location.point else Point(0, 0)


def str_to_bool(string):
    return True if string == 'true' else False
