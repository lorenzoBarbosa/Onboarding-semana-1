import os
from fastapi import FastAPI
import uvicorn

import cadastro_routes
from usuario_repo import criar_tabela


app = FastAPI()
criar_tabela()
app.include_router(cadastro_routes.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

