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

@Monthly_Fee_Router.get("/Get_Monthly_Fee")
async def View_Monthly_Fee(month:int = None,
                           year: int = None,
                           description: str = None,
                           status: str = None,
                           category: str = None,
                           date: date = None,
                           credit_card_ID: int = None,
                           session: Session = Depends(init_session)):
    monthly_fee = {Monthly_Fee.Date: date,
                   extract("year",Monthly_Fee.Date): year,
                   extract("month",Monthly_Fee.Date): month,
                   Monthly_Fee.Category: category,
                   Monthly_Fee.Credit_card_ID: credit_card_ID,
                   Monthly_Fee.Status: status,
                   Monthly_Fee.Description: description
                   }
    for column, value in monthly_fee.items():
        if value is not None:
            invoices = session.query(Monthly_Fee).filter(column == value).all()
        if not monthly_fee:
            raise HTTPException(status_code=400, detail="Mensalidade não encontrado")
    return invoices


@Monthly_Fee_Router.put("/Update_status")
async def Update_Status( 
                    status: str,                 
                    month:int = None,
                    id: int = None,
                    year: int = None,
                    date: date = None,
                    credit_card_ID: int = None,
                    session: Session = Depends(init_session)):
    
    monthly_fee_dict = {
                Monthly_Fee.Date: date,
                extract("year",Monthly_Fee.Date): year,
                extract("month",Monthly_Fee.Date): month,
                Monthly_Fee.Credit_card_ID: credit_card_ID,
                Monthly_Fee.ID: id
                   }
    monthly_fee = None
    for column, value in monthly_fee_dict.items():
        if value is not None:
            monthly_fee = session.query(Monthly_Fee).filter(column == value).all()
        if monthly_fee is None:
            raise HTTPException (status_code=400, detail="Id não encontrado")
        if monthly_fee.Status == "PAGO":
            raise HTTPException(status_code=400, detail="Mensalidade já paga")
        if status == "PAGO":
            monthly_fee.Status = status
            await add_to_expense(value=monthly_fee.Monthly_Value, entry_date=date.today(),session=session, description=monthly_fee.Description, Category=monthly_fee.Category)
            await minus_invoices(value=monthly_fee.Monthly_Value,entry_date=date.today(),session=session)

@Monthly_Fee_Router.put("/Update_infos")
async def Update_infos(
                    scheme: Update_Monthly_Fee_Scheme,
                    month:int = None,
                    id: int = None,
                    year: int = None,
                    description: str = None,
                    status: str = None,
                    category: str = None,
                    date: date = None,
                    credit_card_ID: int = None,
                    session: Session = Depends(init_session)):
    
    monthly_fee_dict = {
                Monthly_Fee.Date: date,
                extract("year",Monthly_Fee.Date): year,
                extract("month",Monthly_Fee.Date): month,
                Monthly_Fee.Category: category,
                Monthly_Fee.Credit_card_ID: credit_card_ID,
                Monthly_Fee.Status: status,
                Monthly_Fee.Description: description,
                Monthly_Fee.ID: id
                   }
    monthly_fee = None
    if year and month is not None:
        monthly_fee = session.query(Monthly_Fee).filter(extract("year",Monthly_Fee.Date) >= year,extract("month",Monthly_Fee.Date) >= month).all()
        for i in monthly_fee:
            i.Description = scheme.Description,
            i.Category = scheme.Category,
            i.Date = scheme.Date,
            i.Status = scheme.Status,
            i.Monthly_Value = scheme.Monthly_Value
        session.commit()
        return{"message": "Informações atualizadas com sucesso",
               "Mensalidades": monthly_fee}
    else:
        for column, value in monthly_fee_dict.items():
            if value is not None:
                monthly_fee = session.query(Monthly_Fee).filter(column == value).all()
                for i in monthly_fee:
                    i.Description = scheme.Description
                    i.Category = scheme.Category
                    i.Date = scheme.Date
                    i.Status = scheme.Status
                    i.Monthly_Value = scheme.Monthly_Value
        session.commit()
    if not monthly_fee_dict:
        raise HTTPException(status_code=400, detail="Mensalidade não encontrado")

    return{"message": "Mensalidade atualizada com sucesso",
           "Dados": monthly_fee}
