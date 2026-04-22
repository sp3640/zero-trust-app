from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="Zero Trust Demo API", version="1.0.0")


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


class ItemResponse(BaseModel):
    id: int
    name: str
    message: str


@app.get("/", response_model=HealthResponse)
def root():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=os.getenv("APP_ENV", "production"),
    )


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=os.getenv("APP_ENV", "production"),
    )


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    return ItemResponse(
        id=item_id,
        name=f"Item {item_id}",
        message="Zero-trust pipeline verified this image before running it.",
    )
