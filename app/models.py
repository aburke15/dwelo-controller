from pydantic import BaseModel


class ThermostatValue(BaseModel):
    temperature_value: int = 73
