from fastapi import APIRouter, Depends
from Models.Models import Monthly_Fee
from sqlalchemy.orm import Session
from sqlalchemy import extract
from Dependecies.Dependecies import init_session
from datetime import date
from Schemes.Monthly_Fee_scheme import Update_Monthly_Fee_Scheme
Monthly_Fee_Router = APIRouter(prefix="/Monthly_Fee", tags=["Monthly_Fee"])


@Monthly_Fee_Router.get("/View_Monthly_Fee{month}")
async def View_Monthly_Fee(month:int,session:Session = Depends(init_session)):
    invoices_month = session.query(Monthly_Fee).filter(extract('month',Monthly_Fee.Date) == month).all()
    return invoices_month

@Monthly_Fee_Router.get("/View_Monthly_Fee{year}")
async def View_Monthly_Fee(year:int,session:Session = Depends(init_session)):
    invoices_year = session.query(Monthly_Fee).filter(extract('year',Monthly_Fee.Date) == year).all()
    return invoices_year


@Monthly_Fee_Router.put("/Update_Monthly_Fee{id}")
async def Update_Monthly_Fee(id:int, scheme: Update_Monthly_Fee_Scheme, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(Monthly_Fee.ID == id).first()
    monthly_fee.Description = scheme.Description
    monthly_fee.Date = scheme.Date
    monthly_fee.Category = scheme.Category
    monthly_fee.Monthly_Value = scheme.Monthly_Value
    monthly_fee.Status = scheme.Status
    session.commit()
    return{"message": "Mensalidade atualizada com sucesso",
           "Dados": monthly_fee}

@Monthly_Fee_Router.put("/Update_Greater_than_month_Year_Monthly_Fee")
async def Update_Monthly_Fee(year:int, month:int, scheme: Update_Monthly_Fee_Scheme, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(extract("year",Monthly_Fee.Date) >= year,extract("month",Monthly_Fee.Date) >= month).all()
    for i in monthly_fee:
        i.Description = scheme.Description
        i.Date = scheme.Date
        i.Category = scheme.Category
        i.Monthly_Value = scheme.Monthly_Value
        i.Status = scheme.Status
    session.commit()
    return{"message": "Mensalidade atualizada com sucesso",
           "Dados": monthly_fee}

@Monthly_Fee_Router.get("/View_Greater_than_month_Year_Monthly_Fee")
async def Update_Monthly_Fee(year: int,month:int, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(extract("year",Monthly_Fee.Date) >= year,extract("month",Monthly_Fee.Date) >= month).all()
    return monthly_fee