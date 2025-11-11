from sqlalchemy import create_engine, Column, Date,  Integer, String, Integer, Float,ForeignKey
from sqlalchemy.orm import declarative_base, relationship

db = create_engine("postgresql://postgres:pgadmin@localhost:5432/Finances"
)
base = declarative_base()


class Credit_card (base):
    __tablename__ = "Credit_card"


    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    Description = Column("Description", String)
    Monthly_Value = Column("Monthly_Value", Float)
    Monthly_Fee  = Column("Monthly_Fee", Integer)
    Total_Value = Column("Total_Value", Float)
    Date = Column("Date", Date)
    Category = Column("Category", String)
    def __init__(self, Description, Monthly_Value, Monthly_Fee, Total_Value, Date, Category):
        
        self.Description = Description
        self.Monthly_Value = Monthly_Value
        self.Monthly_Fee = Monthly_Fee
        self.Total_Value = Total_Value
        self.Date = Date
        self.Category = Category

class Monthly_Fee (base):
    __tablename__ = "Monthly_Fee"


    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    Description = Column("Description", String)
    Monthly_Value = Column("Monthly_Value", Float)
    Credit_card_ID = Column("Credit_card_ID", ForeignKey("Credit_card.ID") )
    Date = Column("Date", Date)
    Status = Column("Status", String)
    Category = Column("Category", String)
    def __init__(self, Description, Monthly_Value, Credit_card_ID, Date, Status, Category):
        
        self.Description = Description
        self.Monthly_Value = Monthly_Value
        self.Date = Date
        self.Credit_card_ID = Credit_card_ID
        self.Status = Status
        self.Category = Category

class Expenses  (base):
    __tablename__="Expenses"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    Description = Column("Description", String)
    Value = Column("Value", Float)
    Date = Column("Date", Date)
    Category = Column("Category", String)

    def __init__ (self, Description, Value, Date, Category):
        self.Description = Description
        self.Value = Value
        self.Date = Date
        self.Category = Category

class Payment(base):
    __tablename__ = "Payment"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    Description = Column("Description", String)
    Value = Column("Value", Float)
    Date = Column("Date", Date)

    def __init__ (self, Description, Value, Date):
        self.Description = Description
        self.Value = Value
        self.Date = Date

class Management(base):
    __tablename__="Management"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    Current_Balance = Column("Current_Balance", Float)
    Current_Invoice = Column("Current_Invoice", Float)
    Date = Column("Date", Date)

    def __init__(self, Current_Balance, Current_Invoice, Date):
        self.Current_Balance = Current_Balance
        self.Current_Invoice = Current_Invoice
        self.Date = Date