from pydantic import BaseModel
from typing import Optional
from datetime import date
class Payment_Scheme (BaseModel):
    Description : str
    Value : float
    Date : date
    class Config:
        from_attributes = True

class Update_Payment_Scheme (BaseModel):
    Description : str
    Value : float
    Date : date
    class Config:
        from_attributes = True