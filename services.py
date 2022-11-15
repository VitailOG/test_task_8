import json
import httpx
from redis import Redis

from config import API_KEY


async def _fetch_data(url: str) -> dict:
    async with httpx.AsyncClient(base_url='https://maps.googleapis.com/maps/api/geocode') as client:
        response = await client.get(url)
        return response.json()


async def city_name_by_geo(city_name: str, redis: Redis):
    url = f'/json?address={city_name}&key={API_KEY}'
    city_name = city_name.lower()
    geo_data = redis.get(city_name)

    # Check exist key in redis
    if geo_data is not None:
        return json.loads(geo_data)

    api_response_data = await _fetch_data(url)  # fetch data from google maps api
    location = api_response_data['results'][0]['geometry']['location']  # parse location from response
    redis.set(city_name, json.dumps(location), 500)
    return location
