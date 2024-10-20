from fastapi import FastAPI
from routers import products, categories
from database import engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(categories.router)


@app.get("/")
def root():
    return {"detail": "Hello World"}