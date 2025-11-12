from fastapi import FastAPI 
from fastapi_mcp import FastApiMCP


app = FastAPI()
mcp = FastApiMCP(app)
mcp.mount_http()

from Routes.Expenses_Routes import Expenses_Router
from Routes.Credit_card_Routes import Credit_card_Router
from Routes.Payment_Routes import Payment_Router
from Routes.Management_Routes import Management_Router
from Routes.Monthly_Fee import Monthly_Fee_Router

app.include_router(Expenses_Router)
app.include_router(Credit_card_Router)
app.include_router(Payment_Router)
app.include_router(Management_Router)
app.include_router(Monthly_Fee_Router)


mcp.setup_server()