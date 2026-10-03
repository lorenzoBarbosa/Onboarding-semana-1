import sqlite3

from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx

from usuario_model import Usuario
import usuario_repo
N8N_URL = "http://localhost:5678/webhook/cadastro" 

router = APIRouter()
templates= Jinja2Templates(directory="templates")



async def notificar_n8n(id_usuario: int, email: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resposta = await client.post(N8N_URL, json={"id": id_usuario, "email": email})

        if resposta.status_code == 400:
            return "invalido"

        resposta.raise_for_status() 
        return "ok"

    except httpx.HTTPError:
        print("N8N não está disponível. Cadastro realizado, mas não foi possível enviar os dados para o n8n.")
        return "indisponivel"



@router.get("/")
async def get_cadastro( ):
    return templates.TemplateResponse("form.html", {"request": {}})

@router.post("/cadastro")
async def post_cadastro(email:str = Form(...)):
    usuario = Usuario(
        id=0,
        email = email
    )
    id_usuario = 0
    mensagem = await notificar_n8n(id_usuario, email)

    try:
        if mensagem == "ok":
                id_usuario = usuario_repo.inserir_usuario(usuario)
                return JSONResponse({"status": "sucesso", "mensagem": "Cadastro realizado com sucesso."})
        elif mensagem == "invalido":
            return JSONResponse({"status": "erro", "mensagem": "E-mail inválido."}, status_code=400)
        elif mensagem == "indisponivel":
            return JSONResponse({"status": "aviso", "mensagem": "Cadastro realizado, mas o n8n não está disponível."})
        
    except sqlite3.IntegrityError:
        return JSONResponse(
            {"status": "erro", "mensagem": "E-mail já cadastrado."}, status_code=400,
            )

    




    return templates.TemplateResponse("form.html", {"request": {}})

