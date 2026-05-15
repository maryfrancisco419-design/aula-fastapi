from sqlalchemy.orm import Session
from models import Curso
from schemas import CursoCreate, CursoUpdate


# ── CREATE ──────────────────────────────────
def criar_curso(db: Session, dados: CursoCreate) -> Curso:
    curso = Curso(**dados.model_dump())   # converte schema → model
    db.add(curso)
    db.commit()
    db.refresh(curso)   # atualiza o objeto com o id gerado
    return curso


# ── READ (todos) ────────────────────────────
def listar_cursos(db: Session) -> list[Curso]:
    return db.query(Curso).all()


# ── READ (por id) ───────────────────────────
def buscar_curso(db: Session, curso_id: int) -> Curso | None:
    return db.query(Curso).filter(Curso.id == curso_id).first()


# ── UPDATE ──────────────────────────────────
def atualizar_curso(db: Session, curso_id: int, dados: CursoUpdate) -> Curso | None:
    curso = buscar_curso(db, curso_id)
    if not curso:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(curso, campo, valor)
    db.commit()
    db.refresh(curso)
    return curso


# ── DELETE ──────────────────────────────────
def deletar_curso(db: Session, curso_id: int) -> bool:
    curso = buscar_curso(db, curso_id)
    if not curso:
        return False
    db.delete(curso)
    db.commit()
    return True