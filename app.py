from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from database import init_db, SessionLocal, AnalysisHistory
from code_analyzer import CodeOptimizerLLM
from sqlalchemy.future import select

app = FastAPI()

# Inicializa o banco de dados
#init_db()
@app.on_event("startup")
async def startup_event():
    await init_db()

# Inicializa o modelo LLM
llm = CodeOptimizerLLM()

class CodeRequest(BaseModel):
    code: str

class CrewAIEvent(BaseModel):
    event_type: str
    payload: CodeRequest

# Remove sugestões duplicadas
def remove_duplicate_suggestions(suggestions: list) -> list:
        return list(set(suggestions.split('\n')))

# Endpoint que gera as sugestões dado um trecho de código
@app.post("/analyze-code")
async def analyze_code_endpoint(code_request: CodeRequest):
    code = code_request.code

    async with SessionLocal() as db:
    
        # Usar o modelo LLM para gerar sugestões
        llm_suggestions = llm.generate_suggestions(code)
        
        # Salvar análise no banco de dados
        #db: Session = SessionLocal()
        analysis_entry = AnalysisHistory(code_snippet=code, suggestions=llm_suggestions)
        db.add(analysis_entry)
        await db.commit()
        await db.refresh(analysis_entry)
        #db.close()
    
    return {"suggestions": remove_duplicate_suggestions(llm_suggestions)}

# Endpoint que recebe eventos do CrewAI, e se for de analize de código, gera as sugestões
@app.post("/crewai/event")
async def crewai_event(event_request: CrewAIEvent):
    if event_request.event_type != "analyze-code":
        raise HTTPException(status_code=400, detail="Tipo de evento inválido. Esperado: 'analyze-code'.")

    # Se o evento for do tipo 'analyze-code', executa a lógica de análise
    async with SessionLocal() as db:
        code = event_request.payload.code
        llm_suggestions = llm.generate_suggestions(code)
        analysis_entry = AnalysisHistory(code_snippet=code, suggestions=llm_suggestions)
        db.add(analysis_entry)
        await db.commit()
        await db.refresh(analysis_entry)

    return {"status": "success", "result": llm_suggestions}

# Endpoint que retorna todas as análises realizadas
@app.get("/analyzes/")
async def get_analyzes():
    async with SessionLocal() as db:
        result = await db.execute(select(AnalysisHistory))
        analyses = result.scalars().all()
        return [{"id": a.id, "code_snippet": a.code_snippet, "suggestions": a.suggestions, "created_at": a.created_at} for a in analyses]

# Endpoint de health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}


#uvicorn app:app --reload

#curl -X GET http://localhost:8000/health

#curl -X POST http://localhost:8000/analyze-code -H "Content-Type: application/json" -d "{\"code\": \"def example_function(n):\n    result = []\n    for i in range(n):\n        result.append(i * i)\n    return result\"}"
""""
def example_function(n):
    result = []
    for i in range(n):
        result.append(i * i)
    return result
"""

#curl -X POST http://localhost:8000/crewai/event -H "Content-Type: application/json" -d "{\"event_type\": \"analyze-code\", \"payload\": {\"code\": \"def example_function(n):\\n    result = []\\n    for i in range(n):\\n        result.append(i * i)\\n    return result\"}}"

#curl -X GET http://localhost:8000/analyzes/