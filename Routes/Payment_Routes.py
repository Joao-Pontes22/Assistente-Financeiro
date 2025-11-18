from fastapi import APIRouter, Depends, HTTPException
from Dependecies.Dependecies import init_session
from sqlalchemy.orm import Session
from sqlalchemy import extract
from Schemes.Payment_scheme import Payment_Scheme, Update_Payment_Scheme
from Models.Models import Payment, Management
from datetime import datetime, date
Payment_Router = APIRouter(prefix="/Payment", tags=["Payment"])



async def add_payment_to_management(value:float, date:str, session:Session):
    current_balance = session.query(Management).order_by(Management.ID.desc()).first()
    updated_balance = current_balance.Current_Balance + value
    if not current_balance:
        new_management = Management(Current_Balance= value,
                                    Date=date,
                                    Current_Invoice=0)
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
    new_payment = Payment(Description=scheme.Description.upper(),
                          Value=scheme.Value,
                          Date=date)
    session.add(new_payment)
    await add_payment_to_management(value=scheme.Value,session=session, date=scheme.Date)
    session.commit()
    return{"message": "Pagamento adicionado com sucesso",
           "Dados": new_payment}

@Payment_Router.put("/Update_Payment")
async def Update_Payment(scheme: Update_Payment_Scheme,
                         id:str = None, 
                         description: str = None,
                         date: date = None,
                         month: int = None,
                         year: int = None,  
                         session:Session = Depends(init_session)):
    query = session.query(Payment)
    if id is not None:
        query = query.filter(Payment.ID == id)
    if description is not None:
        query = query.filter(Payment.Description == description)
    if date is not None:
        query = query.filter(Payment.Date == date)
    if year is not None:
        query = query.filter(extract('year',Payment.Date) == year)
    if month is not None:
        query = query.filter(extract('year',Payment.Date) == month)

    payment = query.all()
    if payment is None:
        raise HTTPException(status_code=400, detail="Pagamento não encontrado")
    
    for i in payment:
        i.Description = scheme.Description.upper()
        i.Date= scheme.Date
        i.Value = scheme.Value
    session.commit()
    return{"message": "Pagamento atualizado com sucesso"}
    
@Payment_Router.get("/Get_all_Payment")
async def View_Payment(session:Session = Depends(init_session)):
    payment = session.query(Payment).all()
    return {"Pagamentos":payment}

@Payment_Router.get("/Get_payment")
async def get_payment(id:int = None,
                      description: str = None,
                      date: date = None,
                      month: int = None,
                      year: int = None,
                      session: Session = Depends(init_session)
                      ):
    query = session.query(Payment)
    if id is not None:
        query = query.filter(Payment.ID == id)
    if description is not None:
        query = query.filter(Payment.Description == description)
    if date is not None:
        query = query.filter(Payment.Date == date)
    if year is not None:
        query = query.filter(extract('year',Payment.Date) == year)
    if month is not None:
        query = query.filter(extract('year',Payment.Date) == month)

    payment = query.all()
    if payment is None:
        raise HTTPException(status_code=400, detail="Pagamento não encontrado")
    return {"Pagamentos": payment}

@Payment_Router.delete("/Delete_Payment")
async def Delete_Payment(id: int, session:Session = Depends(init_session)):
    payment = session.query(Payment).filter(Payment.ID == id).first()
    session.delete(payment)
    session.commit()
    return{"message": "Pagamento deletado com sucesso"}

@Payment_Router.delete("/Delete_ALL_Payment")
async def Delete_all_Payment(session:Session = Depends(init_session)):
    payment = session.query(Payment).all()
    for i in payment:
        session.delete(i)
    session.commit()
    return{"message": "Pagamentos deletados com sucesso"}