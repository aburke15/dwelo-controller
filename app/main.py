from fastapi import FastAPI
from fastapi import APIRouter
import httpx
from app import routes
from app import models
from app import secrets

app = FastAPI()
router = APIRouter()

# use secrets manager or store in db
headers = {"Authorization": secrets.TOKEN}


@app.get("/api/login/")
async def login():
    # use secrets manager
    body = {
        "email": secrets.EMAIL,
        "password": secrets.PASSWORD,
        "applicationId": "concierge"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE}{routes.LOGIN}/", json=body)
        print(res.status_code)
        return res.json()


@app.get("/api/devicelist/")
async def get_device_list():

    async with httpx.AsyncClient() as client:
        res = await client.get(url=f"{routes.DWELO_BASE}{routes.DEVICE_LIST}", headers=headers)
        print(res.status_code)
        return res.json()


@app.post("/api/thermostat/heat/on/")
async def activate_heat():
    body = {"command": "heat"}

    command = routes.COMMAND.replace("deviceId", str(192821))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/thermostat/heat/off/")
async def deactivate_heat():
    body = {"command": "off"}

    command = routes.COMMAND.replace("deviceId", str(192821))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/thermostat/heat/value/")
async def set_heat_temperature_value(temp: models.ThermostatValue):
    print(temp.temperature_value)
    body = {"command": "heat", "commandValue": temp.temperature_value}

    command = routes.COMMAND.replace("deviceId", str(192821))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.get("/api/lighting/entryway/off/")
async def turn_off_entry_way_light():
    body = {"command": "off"}

    command = routes.COMMAND.replace("deviceId", str(192819))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.get("/api/lighting/entryway/on/")
async def turn_on_entry_way_light():
    body = {"command": "on"}

    command = routes.COMMAND.replace("deviceId", str(192819))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.get("/api/lighting/livingroom/on/")
async def turn_on_living_room_light():
    body = {"command": "on"}

    # TODO: move the device list to a db
    data = await get_device_list()

    devices = data["results"]

    rooms = filter(
        lambda device: "living" in device["givenName"].lower(), devices)

    command = ''
    for living_room in rooms:
        print("ROOM:", living_room)
        command = routes.COMMAND.replace("deviceId", str(living_room["uid"]))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()
