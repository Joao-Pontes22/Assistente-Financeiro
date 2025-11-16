from pydantic import BaseModel
from typing import Optional
from datetime import date

class Management_Scheme (BaseModel):
    Current_Balance: float
    Current_Invoice: float
    Date: date
    class Config:
        orm_mode = True