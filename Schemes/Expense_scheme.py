from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class Expense_scheme (BaseModel):
    Description: str
    Value:  float
    Date: date
    Category: str
    class Config:
        from_attributes = True

class Update_Expense_scheme (BaseModel):
    Description: str
    Value: float   
    Date:date
    Category:str

    class Config:
        from_attributes = True
