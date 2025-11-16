from fastapi import APIRouter, Depends, HTTPException
from Models.Models import Monthly_Fee, Management, Expenses
from sqlalchemy.orm import Session
from sqlalchemy import extract
from Dependecies.Dependecies import init_session
from datetime import date
from Schemes.Monthly_Fee_scheme import Update_Monthly_Fee_Scheme
from Schemes.Expense_scheme import Expense_scheme
from Routes.Expenses_Routes import add_expense
Monthly_Fee_Router = APIRouter(prefix="/Monthly_Fee", tags=["Monthly_Fee"])

async def minus_invoices(value: float, entry_date: str, session: Session):
    last_management = (
        session.query(Management)
        .order_by(Management.ID.desc())
        .first()
    )

    # Atualiza os valores
    if last_management.Current_Invoice <= 0:
        new_invoice = 0
    else:
        new_invoice = last_management.Current_Invoice - value
    new_balance = last_management.Current_Balance - value
    # Cria novo registro
    new_management = Management(
        Current_Balance=new_balance,
        Current_Invoice=new_invoice,
        Date=entry_date or date.today()
    )

    session.add(new_management)
    session.commit()
    session.refresh(new_management)

    return {
        "message": "Gestão atualizada com sucesso.",
        "data": {
            "Saldo_atual": float(new_management.Current_Balance),
            "Fatura_atual": float(new_management.Current_Invoice),
            "Data": str(new_management.Date)
        }
    }
async def add_to_expense(value:float, entry_date: date, description: str, Category:str, session:Session):
    new_expense = Expenses(Description="Mensalidade:" + description,
                           Value=value,
                           Date=entry_date,
                           Category="Cartão de crédito:" + Category)
    session.add(new_expense)
    session.commit()
    return{"message": "Despesa adicionado com sucesso",
           "Despesa": new_expense}

@Monthly_Fee_Router.get("/View_Fee_month")
async def View_Monthly_Fee(month:int,session:Session = Depends(init_session)):
    invoices_month = session.query(Monthly_Fee).filter(extract('month',Monthly_Fee.Date) == month).all()
    return invoices_month
    
@Monthly_Fee_Router.get("/View_all_Monthly_Fee")
async def View_Monthly_Fee(session:Session = Depends(init_session)):
    invoices_month = session.query(Monthly_Fee).all()
    return invoices_month

@Monthly_Fee_Router.get("/View_Fee_year")
async def View_Monthly_Fee(year:int,session:Session = Depends(init_session)):
    invoices_year = session.query(Monthly_Fee).filter(extract('year',Monthly_Fee.Date) == year).all()
    return invoices_year


@Monthly_Fee_Router.put("/Update_status")
async def Update_Status(id:int, status:str, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(Monthly_Fee.ID == id).first()
    if not monthly_fee:
        raise HTTPException (status_code=400, detail="Id não encontrado")
    if monthly_fee.Status == "PAGO":
        raise HTTPException(status_code=400, detail="Mensalidade já paga")
    if status == "PAGO":
        monthly_fee.Status = status
        await add_to_expense(value=monthly_fee.Monthly_Value, entry_date=date.today(),session=session, description=monthly_fee.Description, Category=monthly_fee.Category)
        await minus_invoices(value=monthly_fee.Monthly_Value,entry_date=date.today(),session=session)
    session.commit()
    return{"message": "Mensalidade paga com sucesso",
           "Dados": monthly_fee}

@Monthly_Fee_Router.put("/Update_infos")
async def Update_infos(year:int, month:int, scheme: Update_Monthly_Fee_Scheme, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(extract("year",Monthly_Fee.Date) >= year,extract("month",Monthly_Fee.Date) >= month).all()
    if not monthly_fee:
        raise HTTPException(status_code=400, detail="Mensalidade dentro do periodo especificado não encontrado")
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
async def View_Per_year_month(year: int,month:int, session:Session = Depends(init_session)):
    monthly_fee = session.query(Monthly_Fee).filter(extract("year",Monthly_Fee.Date) >= year,extract("month",Monthly_Fee.Date) >= month).all()
    return monthly_fee
