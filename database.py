from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados SQLite
# O arquivo cursos.db será criado automaticamente na pasta do projeto
DATABASE_URL = "sqlite:///./cursos.db"

# Cria o "motor" de conexão com o banco
bd = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite
)

# Fábrica de sessões — cada requisição abrirá uma sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=bd)

# Base para os modelos ORM
Base = declarative_base()


# Função geradora de sessão (usada via Depends no FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db          # entrega a sessão para a rota
    finally:
        db.close()        # sempre fecha ao terminar