from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os


DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD") #export DATABASE_PASSWORD="1234"

# Configuração do banco de dados
#DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost/code_analyzer_db"
DATABASE_URL = f"postgresql+asyncpg://postgres:{DATABASE_PASSWORD}@localhost/code_analyzer_db"


#Base = declarative_base()
#engine = create_engine(DATABASE_URL)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Definição do modelo da tabela
class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    code_snippet = Column(String, nullable=False)
    suggestions = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Função para criar a tabela
#def init_db():
#    Base.metadata.create_all(bind=engine)

# Função para inicializar a tabela 
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Installation Directory: C:\Program Files\PostgreSQL\17
# Server Installation Directory: C:\Program Files\PostgreSQL\17
# Data Directory: C:\Program Files\PostgreSQL\17\data
# Database Port: 5432
# Database Superuser: postgres
# Operating System Account: NT AUTHORITY\NetworkService
# Database Service: postgresql-x64-17
# Command Line Tools Installation Directory: C:\Program Files\PostgreSQL\17
# pgAdmin4 Installation Directory: C:\Program Files\PostgreSQL\17\pgAdmin 4
# Stack Builder Installation Directory: C:\Program Files\PostgreSQL\17
# Installation Log: C:\Users\rodri\AppData\Local\Temp\install-postgresql.log
