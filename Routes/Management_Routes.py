from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract
from Models.Models import Management
from Routes.Credit_card_Routes import update_invoice
from Dependecies.Dependecies import init_session
from Schemes.Management_scheme import Management_Scheme
from datetime import date
Management_Router = APIRouter(prefix="/Management", tags=["Management"])

@Management_Router.get("Get_in_moment_Management")
async def View_Management(session:Session = Depends(init_session)):
    management = session.query(Management).order_by(Management.ID.desc()).first()
    return management
@Management_Router.get("Get_defined_Management")
async def get_defined_management(
    year: int = None,
    month: int = None,
    date: date = None,
    session:Session = Depends(init_session)
    ):
    await update_managament(session=session)
    query = session.query(Management)
    
    if year is not None:
        query.filter(extract('year', Management.Date)== year)
    if month is not None:
        query.filter(extract('year', Management.Date)== month)
    if date is not None:
        query.filter(Management.Date)
    management = query.all()
    return management

@Management_Router.post("Update_balance_and_invoices")
async def update_management(scheme: Management_Scheme, session:Session = Depends(init_session)):
    new_update = Management(Current_Balance=scheme.Current_Balance,
                            Current_Invoice=scheme.Current_Invoice,
                            Date=scheme.Date)
    session.add(new_update)
    session.commit()
    return {"message": "Atualização realizada com sucesso",
            "Saldo": new_update.Current_Balance,
            "Divida": new_update.Current_Invoice}

@Management_Router.delete("/delete_all")
async def delete_all(session:Session = Depends(init_session)):
    management = session.query(Management).all()
    for i in management:
        session.delete(i)
    session.commit()
    return{"message": "Deletados"}

@Management_Router.put("/Update_Management", response_model=Management_Scheme)
async def update_managament(session:Session = Depends(init_session)):
    await update_invoice(entry_date=date.today(),session=session)
    last_management = session.query(Management).order_by(Management.ID.desc()).first()
    return last_management