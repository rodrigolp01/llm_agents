# create_tables.py

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio


# URL do banco de dados
DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost/code_analyzer_db"

## Criação do motor assíncrono
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Criação da base declarativa
Base = declarative_base()

# Definição do modelo da tabela
class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    code_snippet = Column(String, nullable=False)
    suggestions = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Função para criar as tabelas
async def create_tables():
    async with async_engine.begin() as conn:
        # Criação das tabelas
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas com sucesso!")

# Função principal para executar o loop de eventos
def main():
    asyncio.run(create_tables())

if __name__ == "__main__":
    main()
