from fastapi import APIRouter, Depends, HTTPException
from Models.Models import Credit_card, Monthly_Fee, Management
from sqlalchemy.orm import Session
from Schemes.Credit_card_scheme import Credit_card_scheme, Update_Credit_card_scheme
from Schemes.Expense_scheme import Expense_scheme
from Dependecies.Dependecies import init_session
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from sqlalchemy import extract
from Routes.Expenses_Routes import add_expense
Credit_card_Router = APIRouter(prefix="/Credit_card", tags=["Credit_card"])

async def Minus_invoices(value: float, entry_date: str, session: Session):
    last_management = (
        session.query(Management)
        .order_by(Management.Date.desc())
        .first()
    )

    # Atualiza os valores
    new_invoice = last_management.Current_Invoice - value
    # Cria novo registro
    new_management = Management(
        Current_Balance=last_management.Current_Balance,
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
async def sum_invoices(value: float, entry_date: str, session: Session):

    # 1. Converter entry_date corretamente
    if isinstance(entry_date, str):
        entry_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
    elif isinstance(entry_date, datetime):
        entry_date = entry_date.date()
    elif entry_date is None:
        entry_date = date.today()

    # 2. Buscar último registro
    last_management = (
        session.query(Management)
        .order_by(Management.ID.desc())
        .first()
    )

    # 3. Se não existir histórico, criar base
    if not last_management:
        last_management = Management(
            Current_Balance=0,
            Current_Invoice=0,
            Date=entry_date
        )
        session.add(last_management)
        session.commit()
        session.refresh(last_management)

    # 4. Atualizar valores
    new_invoice = last_management.Current_Invoice + value

    # 5. Criar novo registro
    new_management = Management(
        Current_Balance=last_management.Current_Balance,
        Current_Invoice=new_invoice,
        Date=entry_date
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
async def update_invoice(entry_date: date, session: Session):

    # Aceita string ou date
    if isinstance(entry_date, str):
        try:
            entry_date = date.fromisoformat(entry_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Data inválida. Use YYYY-MM-DD")

    today = date.today()
    close_day = 10
    Day_Close_Card = date(today.year, today.month, close_day)

    # Último registro da gestão
    last_management = (
        session.query(Management)
        .order_by(Management.ID.desc())
        .first()
    )

    # Se não existir cria o primeiro
    if not last_management:
        last_management = Management(
            Current_Balance=0,
            Current_Invoice=0,
            Date=entry_date
        )
        session.add(last_management)
        session.commit()
        session.refresh(last_management)

    # Calcular fechamento anterior
    if today.month == 1:
        close_previous = date(today.year - 1, 12, close_day)
    else:
        close_previous = date(today.year, today.month - 1, close_day)

    # Despesas no cartão pendentes
    credit_card = session.query(Credit_card).filter(
        Credit_card.Status == "PENDENTE",
        Credit_card.Date >= close_previous,
        Credit_card.Date <= Day_Close_Card,
        Credit_card.Monthly_Fee == 1        
    ).all()
    total_cc = sum(c.Monthly_Value for c in credit_card)

    # Mensalidades que não são do cartão
    monthly_fee_query = session.query(Monthly_Fee).filter(
        Monthly_Fee.Status == "PENDENTE",
        Monthly_Fee.Date <= Day_Close_Card,
        
    )

    monthly_fee_expense = monthly_fee_query.all()
    total_mf = sum(m.Monthly_Value for m in monthly_fee_expense)

    soma_total = total_cc + total_mf

    nova_fatura = last_management.Current_Invoice = soma_total

    # Cria novo registro
    new_record = Management(
        Current_Balance=last_management.Current_Balance,
        Current_Invoice=nova_fatura,
        Date=entry_date
    )

    session.add(new_record)
    session.commit()

    return {
        "message": "Fatura atualizada com sucesso",
        "Fatura": nova_fatura,
        "Somado": soma_total
    }

async def add_to_monthly_fee(Description: str, Date: str, session:Session):
    expense = session.query(Credit_card).filter(Credit_card.Description == Description, Credit_card.Date == Date).first()
    base_date = expense.Date
    for n in range (expense.Monthly_Fee):
        new_Date = base_date + relativedelta(months=n)
        new_mf = Monthly_Fee(Description=expense.Description,
                         Monthly_Value=expense.Monthly_Value,
                         Credit_card_ID=expense.ID,
                         Date=new_Date,
                         Status="PENDENTE",
                         Category=expense.Category)
        session.add(new_mf)
    session.commit()
    return{"message": "Mensalidade adicionado com sucesso"}

@Credit_card_Router.post("/add_expense_CC")
async def add_expense(scheme: Credit_card_scheme, session:Session =  Depends(init_session)):
    Total = scheme.Monthly_Value * scheme.Monthly_Fee
    new_cc = Credit_card(Description=scheme.Description.upper(),
                         Monthly_Value=scheme.Monthly_Value,
                         Monthly_Fee=scheme.Monthly_Fee,
                         Total_Value=Total,
                         Date=scheme.Date,
                         Category=scheme.Category.upper(),
                         Status="PENDENTE"
                         )
    session.add(new_cc)
    if scheme.Monthly_Fee > 1:
        await add_to_monthly_fee(scheme.Description.upper(), scheme.Date, session)
    await update_invoice(entry_date=scheme.Date, session=session)
    await sum_invoices(value=scheme.Monthly_Value, entry_date=scheme.Date, session=session)
    session.commit()


    return{"message":"Nova despesa do cartão de crédito adicionado",
           "Dados": new_cc}

@Credit_card_Router.put("/Update_expense_cc")
async def Updade_expense( 
                        scheme: Update_Credit_card_scheme,
                        month:int = None,
                        id: int = None,
                        year: int = None,
                        description: str = None,
                        date: date = None,
                        category: str = None,
                        status: str = None,
                        session:Session = Depends(init_session)):
    
    query = session.query(Credit_card)
    upper_status = status.upper() if status is not None else None
    upper_description =  description.upper() if description is not None else None
    upper_category = category.upper() if category is not None else None
    mf = []
    if  id is not None:
        query = query.filter(Credit_card.ID == id)
    if status is not None:
        query = query.filter(Credit_card.Status == upper_status)
    if month is not None:
        query = query.filter(extract('month',Credit_card.Date) == month)
    if year is not None:
        query = query.filter(extract('year',Credit_card.Date) == year)
    if description is not None:
        query = query.filter(Credit_card.Description == upper_description)
    if date is not None:
        query = query.filter(Credit_card.Date == date)
    if category is not None:
        query = query.filter(Credit_card.Category == upper_category)

    expenses = query.first()
    if scheme.Category is not None:
        expenses.Category = scheme.Category.upper()
    if scheme.Date is not None:
        expenses.Date = scheme.Date
    if scheme.Description is not None:
        expenses.Description = scheme.Description.upper()
    if scheme.Monthly_Fee is not None:
        expenses.Monthly_Fee = scheme.Monthly_Fee
    if scheme.Monthly_Value is not None:
        expenses.Monthly_Value = scheme.Monthly_Value
        
    session.commit()
    mf = session.query(Monthly_Fee).filter(Monthly_Fee.Credit_card_ID == expenses.ID).all()
    for i in mf:
        session.delete(i)
    await add_to_monthly_fee(scheme.Description.upper(), scheme.Date, session)
    session.commit()
    return {"message": "Despesas e mensalidades atualizadas com sucesso"}

@Credit_card_Router.delete("/Delete_Expense_cc")
async def Delete_expense(id: str,session:Session = Depends(init_session)):
    expense = session.query(Credit_card).filter(Credit_card.ID == id).first()
    mf = session.query(Monthly_Fee).filter(Monthly_Fee.Credit_card_ID == expense.ID).all()
    session.delete(expense)   
    for i in mf:
        session.delete(i)
    await update_invoice(entry_date=date.today(), session=session)
    session.commit()
    return {"message": "Despesa deletada com sucesso"}
@Credit_card_Router.delete("/Delete_All_Expense_cc")
async def Delete_all_expense(session:Session = Depends(init_session)):
    expense = session.query(Credit_card).all()
    expense_ids = [i.ID for i in expense]
    mf = session.query(Monthly_Fee).filter(Monthly_Fee.Credit_card_ID.in_(expense_ids)).all()
    for i in expense:
        session.delete(i)   
    for i in mf:
        session.delete(i)
    await update_invoice(entry_date=date.today(), session=session)
    session.commit()
    return {"message": "Despesa deletada com sucesso"}


@Credit_card_Router.get("/View_all_expenses_cc")
async def View_all_expenses(session:Session = Depends(init_session)):
    cc = session.query(Credit_card).all()
    mf = session.query(Monthly_Fee).all()
    return {"Cartão de crédito": cc, 
            "Mensalidade": mf}

@Credit_card_Router.get("/View_expenses_cc")
async def View_expenses(month:int = None,
                        id: int = None,
                        year: int = None,
                        description: str = None,
                        date: date = None,
                        category: str = None,
                        status: str = None,
                        session:Session = Depends(init_session)):
    
    query = session.query(Credit_card)
    if  id is not None:
        query = query.filter(Credit_card.ID == id)
    if status is not None:
        query = query.filter(Credit_card.Status == status.upper())
    if month is not None:
        query = query.filter(extract('month',Credit_card.Date) == month)
    if year is not None:
        query = query.filter(extract('year',Credit_card.Date) == year)
    if description is not None:
        query = query.filter(Credit_card.Description == description.upper())
    if date is not None:
        query = query.filter(Credit_card.Date == date)
    if category is not None:
        query = query.filter(Credit_card.Category == category.upper())

    expenses = query.all()
    mf = (
        session.query(Monthly_Fee)
        .filter(Monthly_Fee.Credit_card_ID.in_([e.ID for e in expenses]), 
                extract('year',Monthly_Fee.Date) == year,
                extract('month',Monthly_Fee.Date) == month)
        .all()
        if expenses else []
    )
    return {"Cartão de crédito": expenses, 
            "Mensalidade": mf}

@Credit_card_Router.post("/Pay_invoice")
async def pay_cc(value:float, date:date, session:Session = Depends(init_session)):
    expense_scheme = Expense_scheme(Description="Fatura do Cartão de crédito",
                                    Value=value,
                                    Date=date,
                                    Category="Fatura")
    await add_expense(scheme=expense_scheme,session=session)
    await Minus_invoices(value=value,
                   entry_date=date,
                   session=session)
    session.commit()
    return{"message": "Fatura paga com sucesso",
           "Fatura atual": session.query(Management).order_by(Management.ID.desc()).first()()}
    
