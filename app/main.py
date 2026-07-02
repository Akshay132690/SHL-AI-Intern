from fastapi import FastAPI

print("STEP 1")

from app.agent import SHLAgent

print("STEP 2")

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}