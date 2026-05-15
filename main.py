from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

import models, repository
from database import bd, get_db
from schemas import CursoCreate, CursoUpdate

# Cria as tabelas no banco (se não existirem)
models.Base.metadata.create_all(bind=bd)

app = FastAPI(title="CRUD de Cursos")

# Configura o diretório de templates
templates = Jinja2Templates(directory="templates")


# ── LISTAR todos os cursos ──────────────────
@app.get("/cursos", response_class=HTMLResponse)
def listar(request: Request, db: Session = Depends(get_db)):
    cursos = repository.listar_cursos(db)
    return templates.TemplateResponse(
        request=request,
        name="lista.html",
        context={"cursos": cursos}
    )


# ── FORMULÁRIO de cadastro ──────────────────
@app.get("/cursos/novo", response_class=HTMLResponse)
def form_novo(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="form.html",
        context={"curso": None, "title": "Novo Curso"}
    )


# ── CRIAR curso (recebe dados do formulário) ─
@app.post("/cursos", response_class=HTMLResponse)
def criar(
    request: Request,
    nome:       str   = Form(...),
    descricao:  str   = Form(""),
    carga_hor:  int   = Form(...),
    preco:      float = Form(0.0),
    db: Session = Depends(get_db)
):
    dados = CursoCreate(nome=nome, descricao=descricao,
                        carga_hor=carga_hor, preco=preco)
    repository.criar_curso(db, dados)
    return RedirectResponse("/cursos", status_code=303)


# ── FORMULÁRIO de edição ────────────────────
@app.get("/cursos/{curso_id}/editar", response_class=HTMLResponse)
def form_editar(curso_id: int, request: Request, db: Session = Depends(get_db)):
    curso = repository.buscar_curso(db, curso_id)
    if not curso:
        return RedirectResponse("/cursos", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="form.html",
        context={"curso": curso, "title": "Editar Curso"}
    )


# ── ATUALIZAR curso ─────────────────────────
@app.post("/cursos/{curso_id}/editar", response_class=HTMLResponse)
def atualizar(
    curso_id:   int,
    nome:       str   = Form(...),
    descricao:  str   = Form(""),
    carga_hor:  int   = Form(...),
    preco:      float = Form(0.0),
    db: Session = Depends(get_db)
):
    dados = CursoUpdate(nome=nome, descricao=descricao,
                        carga_hor=carga_hor, preco=preco)
    repository.atualizar_curso(db, curso_id, dados)
    return RedirectResponse("/cursos", status_code=303)


# ── CONFIRMAR exclusão ──────────────────────
@app.get("/cursos/{curso_id}/excluir", response_class=HTMLResponse)
def confirmar_excluir(curso_id: int, request: Request, db: Session = Depends(get_db)):
    curso = repository.buscar_curso(db, curso_id)
    if not curso:
        return RedirectResponse("/cursos", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="confirmar.html",
        context={"curso": curso}
    )


# ── EXCLUIR curso ───────────────────────────
@app.post("/cursos/{curso_id}/excluir", response_class=HTMLResponse)
def excluir(curso_id: int, db: Session = Depends(get_db)):
    repository.deletar_curso(db, curso_id)
    return RedirectResponse("/cursos", status_code=303)


# ── Rota raiz redireciona para /cursos ──────
@app.get("/")
def raiz():
    return RedirectResponse("/cursos")