
from urllib.request import Request
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from usuario_model import Usuario
import usuario_repo

router = APIRouter()
templates= Jinja2Templates(directory="templates")

@router.get("/")
async def get_cadastro(request: Request):
    return templates.TemplateResponse("form.html", {"request": {request}})

@router.post("/cadastro")
async def post_cadastro(request: Request, email:str = Form()):
    usuario = Usuario(
        id=0,
        email = email
    )
    usuario_repo.inserir_usuario(usuario)

    return RedirectResponse(f"/", status_code=303)

