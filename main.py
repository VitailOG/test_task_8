from fastapi import FastAPI, Body

from events import event_wrapper
from requests import CustomRequest
from requests import CustomRoute
from services import city_name_by_geo

app = FastAPI()


app.add_event_handler('startup', event_wrapper(app))
app.router.route_class = CustomRoute


@app.post("/")
async def get_city_name_by_geo(
        request: CustomRequest,
        city_name: str = Body(embed=True)
):
    return await city_name_by_geo(city_name, request.redis)
