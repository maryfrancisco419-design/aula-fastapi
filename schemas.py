from pydantic import BaseModel, Field
from typing import Optional

# Schema base com os campos comuns
class CursoBase(BaseModel):
    nome:       str   = Field(..., min_length=3, max_length=100)
    descricao:  Optional[str] = Field(None, max_length=300)
    carga_hor:  int   = Field(..., gt=0)        # deve ser maior que 0
    preco:      float = Field(0.0, ge=0)        # deve ser >= 0


# Schema para criar um curso (sem id)
class CursoCreate(CursoBase):
    pass


# Schema para atualizar (todos os campos opcionais)
class CursoUpdate(BaseModel):
    nome:       Optional[str]   = None
    descricao:  Optional[str]   = None
    carga_hor:  Optional[int]   = None
    preco:      Optional[float] = None


# Schema de resposta (com id)
class CursoResponse(CursoBase):
    id: int

    class Config:
        from_attributes = True   # permite converter Model → Schema