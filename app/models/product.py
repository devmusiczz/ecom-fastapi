from pydantic import BaseModel
from typing import List

class SizeEntry(BaseModel):
    size: str
    quantity: int

class Product(BaseModel):
    name: str
    price: float
    sizes: List[SizeEntry]
