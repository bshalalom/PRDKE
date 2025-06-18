from fastapi import FastAPI
from backend.routers import analyze_all
from backend.routers import openai_agents
from backend.routers import perplexity_agent

app = FastAPI()

# Binde alle Router ein
app.include_router(analyze_all.router)
app.include_router(openai_agents.router)
app.include_router(perplexity_agent.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
