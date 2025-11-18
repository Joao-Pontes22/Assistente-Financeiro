from fastapi import APIRouter, Depends, HTTPException
from Models.Models import Monthly_Fee, Management, Expenses
from sqlalchemy.orm import Session
from sqlalchemy import extract
from Dependecies.Dependecies import init_session
from datetime import date
from Schemes.Monthly_Fee_scheme import Update_Monthly_Fee_Scheme
from Schemes.Expense_scheme import Expense_scheme
from Routes.Expenses_Routes import add_expense
from Routes.Credit_card_Routes import update_invoice
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
    if new_invoice <= 0 :
        new_management = Management(
        Current_Balance=new_balance,
        Current_Invoice=0,
        Date=entry_date or date.today()
    )
    else:
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
                           id: int =None,
                           year: int = None,
                           description: str = None,
                           status: str = None,
                           category: str = None,
                           date: date = None,
                           credit_card_ID: int = None,
                           session: Session = Depends(init_session)):
    query = session.query(Monthly_Fee)

    if year is not None:
        query = query.filter(extract('year', Monthly_Fee.Date) == year)
    if month is not None:
        query = query.filter(extract('month', Monthly_Fee.Date) == month, )
    if id is not None:
        query = query.filter(Monthly_Fee.ID == id)
    if description is not None:
        query = query.filter(Monthly_Fee.Description == description.upper())
    if category is not None:
        query = query.filter(Monthly_Fee.Category == category.upper())
    if status is not None:
        query = query.filter(Monthly_Fee.Status == status.upper())
    if date is not None:
        query = query.filter(Monthly_Fee.Date == date)
    if credit_card_ID is not None:
        query = query.filter(Monthly_Fee.Credit_card_ID == credit_card_ID)
    
    monthly_fee = query.all()

    if not monthly_fee:
         raise HTTPException(status_code=400, detail="Mensalidade não encontrado")
    return monthly_fee


@Monthly_Fee_Router.put("/Update_status")
async def Update_Status( 
                    status: str,                 
                    month:int = None,
                    id: int = None,
                    year: int = None,
                    credit_card_ID: int = None,
                    session: Session = Depends(init_session)):
    
    query = session.query(Monthly_Fee)

    if month is not None:
        query = query.filter(extract('month', Monthly_Fee.Date) == month)
    if year is not None:
        query = query.filter(extract('year', Monthly_Fee.Date) == year)
    if id is not None:
        query = query.filter(Monthly_Fee.ID == id)
    if credit_card_ID is not None:
        query = query.filter(Monthly_Fee.Credit_card_ID == credit_card_ID)
    
    monthly_fee = query.all()
    for i in monthly_fee:
        if status.upper() == "PAGO" and i.Status == "PAGO":
            continue
        if status.upper() == "PAGO":
            i.Status = status.upper()
            await add_to_expense(value=i.Monthly_Value, entry_date=date.today(),session=session, description=i.Description, Category=i.Category)
            await minus_invoices(value=i.Monthly_Value,entry_date=date.today(),session=session)    
        elif status.upper() == "PENDENTE":
            i.Status = status.upper()
            await update_invoice(entry_date=date.today(), session=session)
    session.commit()
    return{"message": "Mensalidade(s) atualizada(s) com sucesso",
           "Mensaliades": monthly_fee}

@Monthly_Fee_Router.put("/Update_infos_greater_than")
async def Update_infos_greater(
                    scheme: Update_Monthly_Fee_Scheme,
                    month:int = None,               
                    year: int = None,
                    session: Session = Depends(init_session)):
    
    query = session.query(Monthly_Fee)

    if year and month is not None:
        query = query.filter(extract('year', Monthly_Fee.Date) >= year,extract('month', Monthly_Fee.Date) >= month, )
        
    monthly_fee = query.all()
    for i in monthly_fee:
        if scheme.Description is not None:
            i.Description = scheme.Description.upper(),
        if scheme.Category is not None:
         i.Category = scheme.Category.upper(),
        if scheme.Date is not None:
            i.Date = scheme.Date,
        if scheme.Status is not None:
            i.Status = scheme.Status.upper(),
        if scheme.Monthly_Value is not None:
            i.Monthly_Value = scheme.Monthly_Value
        session.commit()
        return{"message": "Informações atualizadas com sucesso",
               "Mensalidades": monthly_fee}
    session.commit()

    if not monthly_fee:
        raise HTTPException(status_code=400, detail="Mensalidade não encontrado")

    return{"message": "Mensalidade atualizada com sucesso",
           "Dados": monthly_fee}

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
    
    query = session.query(Monthly_Fee)

    if year is not None:
        query = query.filter(extract('year', Monthly_Fee.Date) == year)
    if month is not None:
        query = query.filter(extract('month', Monthly_Fee.Date) == month, )
    if id is not None:
        query = query.filter(Monthly_Fee.ID == id)
    if description is not None:
        query = query.filter(Monthly_Fee.Description == description.upper())
    if category is not None:
        query = query.filter(Monthly_Fee.Category == category.upper())
    if status is not None:
        query = query.filter(Monthly_Fee.Status == status.upper())
    if date is not None:
        query = query.filter(Monthly_Fee.Date == date)
    if credit_card_ID is not None:
        query = query.filter(Monthly_Fee.Credit_card_ID == credit_card_ID)

    monthly_fee = query.all()
    for i in monthly_fee:
        if scheme.Description is not None:
            i.Description = scheme.Description.upper(),
        if scheme.Category is not None:
         i.Category = scheme.Category.upper(),
        if scheme.Date is not None:
            i.Date = scheme.Date,
        if scheme.Status is not None:
            i.Status = scheme.Status.upper(),
        if scheme.Monthly_Value is not None:
            i.Monthly_Value = scheme.Monthly_Value
        session.commit()
        return{"message": "Informações atualizadas com sucesso",
               "Mensalidades": monthly_fee}
    session.commit()

    if not monthly_fee:
        raise HTTPException(status_code=400, detail="Mensalidade não encontrado")

    return{"message": "Mensalidade atualizada com sucesso",
           "Dados": monthly_fee}

