from fastapi import APIRouter, Depends
from Models.Models import Monthly_Fee
from sqlalchemy.orm import Session
from sqlalchemy import extract
from Dependecies.Dependecies import init_session
from datetime import date
from Schemes.Monthly_Fee_scheme import Update_Monthly_Fee_Scheme
from Routes.Expenses_Routes import update_management
Monthly_Fee_Router = APIRouter(prefix="/Monthly_Fee", tags=["Monthly_Fee"])


@Monthly_Fee_Router.get("/View_Fee_month")
async def View_Monthly_Fee(month:int,session:Session = Depends(init_session)):
    invoices_month = session.query(Monthly_Fee).filter(extract('month',Monthly_Fee.Date) == month).all()
    return invoices_month
    
@Monthly_Fee_Router.get("/View_Monthly_Fee")
async def View_Monthly_Fee(session:Session = Depends(init_session)):
    invoices_month = session.query(Monthly_Fee).all()
    return invoices_month

@Monthly_Fee_Router.get("/View_Fee_year")
async def View_Monthly_Fee(year:int,session:Session = Depends(init_session)):
    invoices_year = session.query(Monthly_Fee).filter(extract('year',Monthly_Fee.Date) == year).all()
    return invoices_year


@Monthly_Fee_Router.put("/Update_Monthly_Fee_status")
async def Update_Monthly_Fee(id:int, status:str, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(Monthly_Fee.ID == id).first()
    if scheme.Status == "PAGO":
        update_management(value=monthly_fee.Monthly_Value,entry_date=date.today(),session=session)
    session.commit()
    return{"message": "Mensalidade atualizada com sucesso",
           "Dados": monthly_fee}

@Monthly_Fee_Router.put("/Update_fee")
async def Update_Monthly_Fee(year:int, month:int, scheme: Update_Monthly_Fee_Scheme, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(extract("year",Monthly_Fee.Date) >= year,extract("month",Monthly_Fee.Date) >= month).all()
    for i in monthly_fee:
        if i.Description is not None:
            i.Description = scheme.Description
        if i.Date is not None:
            i.Date = scheme.Date
        if i.Category is not None:
            i.Category = scheme.Category
        if i.Monthly_Value is not None:
            i.Monthly_Value = scheme.Monthly_Value
        if i.Status is not None:
            i.Status = scheme.Status
    session.commit()
    return{"message": "Mensalidade atualizada com sucesso",
           "Dados": monthly_fee}

@Monthly_Fee_Router.get("/View_fee")
async def Update_Monthly_Fee(year: int,month:int, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(extract("year",Monthly_Fee.Date) >= year,extract("month",Monthly_Fee.Date) >= month).all()
    return monthly_fee
