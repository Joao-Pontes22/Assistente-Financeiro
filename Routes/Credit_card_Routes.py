from fastapi import APIRouter, Depends
from Models.Models import Credit_card, Monthly_Fee
from sqlalchemy.orm import Session
from Schemes.Credit_card_scheme import Credit_card_scheme, Update_Credit_card_scheme
from Dependecies.Dependecies import init_session
from dateutil.relativedelta import relativedelta

Credit_card_Router = APIRouter(prefix="/Credit_card", tags=["Credit_card"])

Day_Close_Card = 10
Day_Due_Card = 16

def add_to_monthly_fee(Description: str, Date: str, session:Session):
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
    Total = scheme.Value * scheme.Monthly_Fee
    new_cc = Credit_card(Description=scheme.Description,
                         Monthly_Value=scheme.Monthly_Value,
                         Monthly_Fee=scheme.Monthly_Fee,
                         Total_Value=Total,
                         Date=scheme.Date,
                         Category=scheme.Category
                         )
    session.add(new_cc)
    if scheme.Monthly_Fee > 1:
        add_to_monthly_fee(scheme.Description, scheme.Date, session)
    session.commit()


    return{"message":"Nova despesa do cartão de crédito adicionado",
           "Dados": new_cc}

@Credit_card_Router.put("/Update_expense_cc")
async def Updade_expense(id:int,scheme: Update_Credit_card_scheme, session:Session = Depends(init_session)):
    expense = session.query(Credit_card).filter(Credit_card.ID == id).first()
    mf = session.query(Monthly_Fee).filter(Monthly_Fee.Credit_card_ID == expense.ID).all()
    if scheme.Description is not None:
        expense.Description = scheme.Description
    if scheme.Date is not None:
        expense.Date = scheme.Date
    if scheme.Monthly_Value is not None:
        expense.Monthly_Value = scheme.Monthly_Value
    if scheme.Monthly_Fee is not None:
        expense.Monthly_Fee = scheme.Monthly_Fee
    if scheme.Category is not None:
        expense.Category = scheme.Category
    session.commit()
    for i in mf:
        session.delete(i)
    add_to_monthly_fee(scheme.Description, scheme.Date, session)
    session.commit()
    return {"message": "Despesas e mensalidades atualizadas com sucesso"}

@Credit_card_Router.delete("/Delete_Expense_cc")
async def Delete_expense(id: str,session:Session = Depends(init_session)):
    expense = session.query(Credit_card).filter(Credit_card.ID == id).first()
    mf = session.query(Monthly_Fee).filter(Monthly_Fee.Credit_card_ID == expense.ID).all()
    session.delete(expense)   
    for i in mf:
        session.delete(i)
    session.commit()
    return {"message": "Despesa deletada com sucesso"}

@Credit_card_Router.get("/View_all_expenses_cc")
async def View_expenses(session:Session = Depends(init_session)):
    cc = session.query(Credit_card).all()
    mf = session.query(Monthly_Fee).all()
    return {"Cartão de crédito": cc, 
            "Mensalidade": mf}