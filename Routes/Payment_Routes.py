from fastapi import APIRouter, Depends
from Dependecies.Dependecies import init_session
from sqlalchemy.orm import Session
from Schemes.Payment_scheme import Payment_Scheme, Update_Payment_Scheme
from Models.Models import Payment, Management
from Routes.Expenses_Routes import update_management
Payment_Router = APIRouter(prefix="/Payment", tags=["Payment"])


def add_payment_to_management(value:float, date:str, session:Session):
    current_balance = session.query(Management).first()
    updated_balance = current_balance.Current_Balance + value
    if not current_balance:
        new_management = Management(Current_Balance= updated_balance,
                                    Date=date,
                                    Current_Invoice=current_balance.Current_Invoice)
        session.add(new_management)
    new_management = Management(Current_Balance= updated_balance,
                                    Date=date,
                                    Current_Invoice=current_balance.Current_Invoice)
    session.add(new_management)
    session.commit()
    return{"message": "Saldo atualizado com sucesso",   
           "saldo": new_management}

@Payment_Router.post("/add_Payment")
async def add_Payment(scheme: Payment_Scheme, session:Session = Depends(init_session)):
    new_payment = Payment(Description=scheme.Description,
                          Value=scheme.Value,
                          Date=scheme.Date)
    session.add(new_payment)
    add_payment_to_management(value=scheme.Value,session=session, date=scheme.Date)
    session.commit()
    return{"message": "Pagamento adicionado com sucesso",
           "Dados": new_payment}

@Payment_Router.put("/Update_Payment")
async def Update_Payment(id:str,scheme: Update_Payment_Scheme, session:Session = Depends(init_session)):
    payment = session.query(Payment).filter(Payment.ID==id).first()
    if scheme.Description is not None:
        payment.Description = scheme.Description
    if scheme.Date is not None:
        payment.Date = scheme.Date
    if scheme.Value is not None:
        payment.Value = scheme.Value
    update_management(value=scheme.Value, session=session, entry_date=scheme.Date)
    session.commit()
    return{"message": "Pagamento atualizado com sucesso",
           "Descrição": payment.Description,
           "Data": payment.Date,
           "Valor": payment.Value}

@Payment_Router.get("/View_Payment")
async def View_Payment(session:Session = Depends(init_session)):
    payment = session.query(Payment).all()
    return {"Pagamentos":payment}

@Payment_Router.delete("/Delete_Payment")
async def Delete_Payment(id: int, session:Session = Depends(init_session)):
    payment = session.query(Payment).filter(Payment.ID == id).first()
    session.delete(payment)
    session.commit()
    return{"message": "Pagamento deletado com sucesso"}