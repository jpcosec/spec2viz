from dataclasses import dataclass

from pydantic import BaseModel


class Thing(BaseModel):
    name: str


@dataclass
class Settings:
    verbose: bool = False
