from typing import TypedDict
from enum import Enum

CONDITIONS = ("eq", "ne", "gt", "gte", "lt", "lte")
CONDITIONS_MAP = {
    "eq": "=",
    "ne": "!=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<="
}


class Op(str, Enum):
    OR = 'or'
    AND = 'and'


class Condition(TypedDict):
    key: str
    condition: str
    value: str


class BaseFilter:
    def generate(self, condition: Condition):
        return f""
