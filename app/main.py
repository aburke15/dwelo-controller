from fastapi import FastAPI
from fastapi import APIRouter
import httpx
from typing import Union
from app import routes
from app import models
from app import secrets

app = FastAPI()
router = APIRouter()

# use secrets manager or store in db
headers = {"Authorization": secrets.TOKEN}


@app.post("/api/login/")
async def login():
    # use secrets manager
    body = {
        "email": secrets.EMAIL,
        "password": secrets.PASSWORD,
        "applicationId": "concierge"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{routes.LOGIN}", json=body)
        print(res.status_code)
        return res.json()


@app.get("/api/devicelist/")
async def get_device_list():
    async with httpx.AsyncClient() as client:
        res = await client.get(url=f"{routes.DWELO_BASE_URL}{routes.DEVICE_LIST}", headers=headers)
        print(res.status_code)
        return res.json()


@app.post("/api/thermostat/off/")
async def thermostat_off():
    body = {"command": "off"}
    thermostat_id = await get_device_id_by_name("thermostat")
    command = routes.COMMAND.replace("device_id", str(thermostat_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/thermostat/cool/on/")
async def ac_on():
    body = {"command": "cool"}
    thermostat_id = await get_device_id_by_name("thermostat")
    command = routes.COMMAND.replace("device_id", str(thermostat_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/thermostat/cool/value/")
async def set_ac_temperature_value(temp: models.ThermostatValue):
    body = {"command": "cool", "commandValue": temp.temperature_value}
    thermostat_id = await get_device_id_by_name("thermostat")
    command = routes.COMMAND.replace("device_id", str(thermostat_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/thermostat/heat/on/")
async def heat_on():
    body = {"command": "heat"}
    thermostat_id = await get_device_id_by_name("thermostat")
    command = routes.COMMAND.replace("device_id", str(thermostat_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/thermostat/heat/value/")
async def set_heat_temperature_value(temp: models.ThermostatValue):
    body = {"command": "heat", "commandValue": temp.temperature_value}
    thermostat_id = await get_device_id_by_name("thermostat")
    command = routes.COMMAND.replace("device_id", str(thermostat_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/lighting/entryway/on/")
async def turn_on_entry_way_light():
    body = {"command": "on"}
    entry_way_id = await get_device_id_by_name("entry")
    command = routes.COMMAND.replace("device_id", str(entry_way_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/lighting/entryway/off/")
async def turn_off_entry_way_light():
    body = {"command": "off"}
    entry_way_id = await get_device_id_by_name("entry")
    command = routes.COMMAND.replace("device_id", str(entry_way_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/lighting/livingroom/on/")
async def turn_on_living_room_light():
    body = {"command": "on"}
    living_room_id = await get_device_id_by_name("living")
    command = routes.COMMAND.replace("device_id", str(living_room_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/lighting/livingroom/off/")
async def turn_off_living_room_light():
    body = {"command": "off"}
    living_room_id = await get_device_id_by_name("living")
    command = routes.COMMAND.replace("device_id", str(living_room_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/locks/frontdoor/lock/")
async def lock_front_door():
    body = {"command": "lock"}
    front_door_id = await get_device_id_by_name("front")
    command = routes.COMMAND.replace("device_id", str(front_door_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


@app.post("/api/locks/frontdoor/unlock/")
async def unlock_front_door():
    body = {"command": "unlock"}
    front_door_id = await get_device_id_by_name("front")
    command = routes.COMMAND.replace("device_id", str(front_door_id))

    async with httpx.AsyncClient() as client:
        res = await client.post(url=f"{routes.DWELO_BASE_URL}{command}", headers=headers, json=body)
        print(res.status_code)
        return res.json()


async def get_device_id_by_name(name: str) -> Union[int, None]:
    # TODO: move the device list to a db
    device_list = await get_device_list()
    devices = device_list["results"]
    device = filter(lambda dev: name in dev["givenName"].lower(), devices)

    for d in device:
        return d["uid"]

    return None
