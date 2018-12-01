from geopy.geocoders import Yandex

yandex_geocoder = Yandex(lang='ru', user_agent='navalny.notifier')


def get_coordinates(address):
    location = yandex_geocoder.geocode(address, exactly_one=True)
    return location.point if location else None
