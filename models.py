from sqlalchemy import Column, Integer, String, Float
from database import Base

class Curso(Base):
    __tablename__ = "cursos"         # nome da tabela no banco

    id          = Column(Integer, primary_key=True, index=True)
    nome        = Column(String(100), nullable=False)
    descricao   = Column(String(300), nullable=True)
    carga_hor   = Column(Integer, nullable=False)   # em horas
    preco       = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Curso id={self.id} nome={self.nome}>"