from pydantic import BaseModel
from datetime import date

class Update_Monthly_Fee_Scheme (BaseModel):
    Description : str
    Monthly_Value : float
    Date : date
    Status : str
    Category : str
    class Config:
        from_attributes = True
