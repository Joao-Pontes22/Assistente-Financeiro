from pydantic import BaseModel
from typing import Optional
from datetime import date


class Credit_card_scheme (BaseModel):
    Description : str
    Monthly_Value: float
    Monthly_Fee: int
    Date: date
    Category: str
    class Config:
        from_attriutes = True

class Update_Credit_card_scheme (BaseModel):
    Description : str = None
    Monthly_Value: float = None
    Monthly_Fee: int = None
    Date: date = None
    Category:  str = None
    class Config:
        from_attributes = True