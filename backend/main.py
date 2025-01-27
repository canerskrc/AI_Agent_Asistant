from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = "YOUR_OPENAI_API_KEY"

class QueryModel(BaseModel):
    query: str
    context: dict

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Agent Assistant!"}

@app.post("/query")
async def handle_query(query_model: QueryModel):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{query_model.context}: {query_model.query}",
            max_tokens=150
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
