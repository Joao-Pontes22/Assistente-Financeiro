from fastapi import APIRouter, Depends
from Dependecies.Dependecies import init_session
from sqlalchemy.orm import Session
from Schemes.Expense_scheme import Expense_scheme, Update_Expense_scheme
from Models.Models import Expenses, Management, Credit_card, Monthly_Fee
from Response.Expenses_Response import Expense_Responde
from datetime import date

Expenses_Router = APIRouter(prefix="/Exepenses",tags=["Expenses"], )



def update_management(value: float, entry_date: str, session: Session):
    """Atualiza o saldo e fatura corrente no gerenciamento financeiro."""
    today = date.today()
    Day_Close_Card = date(today.year, today.month, 10)
    # Busca o registro mais recente da tabela de gestão
    last_management = (
        session.query(Management)
        .order_by(Management.Date.desc())
        .first()
    )
    if today.month == 1:
        close_previous = date(today.year - 1, 12, Day_Close_Card.day)
    else:
        close_previous = date(today.year, today.month - 1, Day_Close_Card.day)

    credit_card = session.query(Credit_card).filter(Credit_card.Date >= close_previous,
                                                     Credit_card.Date < Day_Close_Card ).all()
    
    total_expense_cc = sum(c.Monthly_Value for c in credit_card)

    monthly_fee_expense = session.query(Monthly_Fee).filter(Monthly_Fee.Date <= Day_Close_Card, Monthly_Fee.Status == "PENDENTE" ).all()
    total_expense_mf = sum(c.Monthly_Value for c in monthly_fee_expense)
    if not last_management:
        # Caso seja a primeira inserção
        current_balance = 0
        current_invoice = 0
    else:
        current_balance = last_management.Current_Balance
        current_invoice = last_management.Current_Invoice

    # Atualiza os valores
    new_balance = current_balance - value
    new_invoice = current_invoice + value + total_expense_cc + total_expense_mf

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
    



@Expenses_Router.post("/add_expense")
async def add_expense(scheme: Expense_scheme, session: Session = Depends(init_session)):
    new_expense = Expenses(Description=scheme.Description,
                           Value=scheme.Value,
                           Date=scheme.Date,
                           Category=scheme.Category)
    session.add(new_expense)
    update_management(value=scheme.Value, session=session, entry_date=scheme.Date )
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

@Expenses_Router.put("/update_expense")
async def update_expense(id:int,scheme:Update_Expense_scheme, session:Session = Depends(init_session)):
    despesa = session.query(Expenses).filter(Expenses.ID == id).first()
    if scheme.Description is not None:
        despesa.Description = scheme.Description
    if scheme.Category is not None:
        despesa.Category = scheme.Category
    if scheme.Value is not None:
        despesa.Value = scheme.Value
    if scheme.Date is not None:
        despesa.Date = scheme.Date
    session.commit()
    return{"message": "Dados atualizado com sucesso",
           "Dados": despesa}

@Expenses_Router.get("View_Expenses")
async def View_Expenses(session:Session = Depends(init_session)):
    expenses = session.query(Expenses).all()
    return{"message": "Lista de despesas carregadas",
           "Dados": expenses}