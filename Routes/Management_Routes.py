from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.Models import Management
from Dependecies.Dependecies import init_session
from Schemes.Management_scheme import Management_Scheme
Management_Router = APIRouter(prefix="/Management", tags=["Management"])

@Management_Router.get("View_Management")
async def View_Management(session:Session = Depends(init_session)):
    management = session.query(Management).all()

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