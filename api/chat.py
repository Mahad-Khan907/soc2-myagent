from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from agents import Runner

# Import the agent logic from the agent_core file
from agent_core import agent, config, Runner

app = FastAPI()

# Pydantic model for request
class ChatRequest(BaseModel):
    message: str

# Allow React frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message is empty")

    try:
        # Await the async runner
        result = await Runner.run(
            agent,
            input=request.message,
            run_config=config,
        )
        return {"response": result.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))