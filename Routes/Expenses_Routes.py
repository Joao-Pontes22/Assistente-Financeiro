from fastapi import APIRouter, Depends, HTTPException
from Dependecies.Dependecies import init_session
from sqlalchemy.orm import Session
from Schemes.Expense_scheme import Expense_scheme, Update_Expense_scheme
from Models.Models import Expenses, Management, Credit_card, Monthly_Fee
from Response.Expenses_Response import Expense_Responde
from datetime import date
from sqlalchemy import extract

Expenses_Router = APIRouter(prefix="/Exepenses",tags=["Expenses"], )



async def minus_expense (value:float, entry_date:date, session:Session):
    inMoment_balance = session.query(Management).order_by(Management.ID.desc()).first()
    if not inMoment_balance:
        new_balance = Management(
            Current_Balance=0 - value,
            Current_Invoice=0,
            Date=entry_date
        )
        session.add(new_balance)
        session.commit()
        return {
            "message": "Primeiro saldo criado",
            "Saldo": new_balance.Current_Balance,
            "Fatura": new_balance.Current_Invoice
        }

    # Caso JÁ exista registro
    new_balance = Management(
        Current_Balance=inMoment_balance.Current_Balance - value,
        Current_Invoice=inMoment_balance.Current_Invoice,
        Date=entry_date
    )

    session.add(new_balance)
    session.commit()

    return {
        "message": "Saldo atualizado com sucesso",
        "Saldo": new_balance.Current_Balance,
        "Fatura": new_balance.Current_Invoice
    }




@Expenses_Router.post("/add_expense")
async def add_expense(scheme: Expense_scheme, session: Session = Depends(init_session)):
    new_expense = Expenses(Description=scheme.Description.upper(),
                           Value=scheme.Value,
                           Date=scheme.Date,
                           Category=scheme.Category.upper())
    session.add(new_expense)
    await minus_expense(value=scheme.Value, session=session, entry_date=scheme.Date )
    session.commit()
    return{"message": "Despesa adicionado com sucesso",
           "dados": new_expense}

@Expenses_Router.delete("/delete_expense")
async def delete_expense(id:int, session:Session = Depends(init_session)):
    despesa = session.query(Expenses).filter(Expenses.ID == id).first()
    session.delete(despesa)
    session.commit()
    return{"message": "Despesa deletada com sucesso",
           "Dados":despesa }


@Expenses_Router.delete("/delete_all_expense")
async def delete_all_expense(session:Session = Depends(init_session)):
    despesa = session.query(Expenses).all()
    for i in despesa:
        session.delete(i)
    session.commit()
    return{"message": "Todas Despesa deletada com sucesso"}

@Expenses_Router.put("/update_expense")
async def update_expense(scheme:Update_Expense_scheme, 
                         
    id: int = None,
    description: str = None,
    category: str = None,
    year:int = None,
    month: int = None,
    date: date = None,
    session:Session = Depends(init_session)
    ):

    query = session.query(Expenses)
    
    if id is not None:
        query = query.filter(Expenses.ID == id)
    if description is not None:
        query = query.filter(Expenses.Description == description.upper())
    if category is not None:
        query = query.filter(Expenses.Category == category.upper())
    if year is not None:
        query = query.filter(extract('year',Expenses.Date) == year)
    if month is not None:
        query = query.filter(extract('month',Expenses.Date) == month)
    if date is not None:
        query = query.filter(Expenses.Date == date)
    
    expenses = query.all()
    for i in expenses:
        if scheme.Description is not None:
            i.Description = scheme.Description
        if scheme.Category is not None:
            i.Category = scheme.Category
        if scheme.Value is not None:
            i.Value = scheme.Value
        if scheme.Date is not None:
            i.Date = scheme.Date
    session.commit()
    return{"message": "Dados atualizado com sucesso",
           "Dados": expenses}

@Expenses_Router.get("View_Expenses")
async def View_Expenses(
    id: int = None,
    description: str = None,
    category: str = None,
    year:int = None,
    month: int = None,
    date: date = None,
    session:Session = Depends(init_session)
    ):

    query = session.query(Expenses)
    
    if id is not None:
        query = query.filter(Expenses.ID == id)
    if description is not None:
        query = query.filter(Expenses.Description == description.upper())
    if category is not None:
        query = query.filter(Expenses.Category == category.upper())
    if year is not None:
        query = query.filter(extract('year',Expenses.Date) == year)
    if month is not None:
        query = query.filter(extract('month',Expenses.Date) == month)
    if date is not None:
        query = query.filter(Expenses.Date == date)
    
    expenses = query.all()
    return{"message": "Lista de despesas carregadas",
           "Dados": expenses}