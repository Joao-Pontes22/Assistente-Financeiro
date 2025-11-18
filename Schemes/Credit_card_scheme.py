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
    Description : str 
    Monthly_Value: float 
    Monthly_Fee: int 
    Date: date 
    Category:  str
    class Config:
        from_attributes = True