from pydantic import BaseModel

class Expense_Responde(BaseModel):
    Description: str
    Value:  float
    Date: str
    Category: str
    class config:
        from_attributes = True