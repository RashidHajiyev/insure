from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from typing import List

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Replace with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Database configuration
conn = psycopg2.connect(
    dbname="insure",
    user="postgres",
    password="swordfish",
    host="localhost",
    port="5432"
)

class Option(BaseModel):
    name: str

@app.get("/", response_model=List[Option])
async def get_options():
    cur = conn.cursor()
    cur.execute('SELECT "colName" FROM public.in_products;')  # Update table and columns as necessary
    rows = cur.fetchall()
    #options = [{"id": row[0], "name": row[1]} for row in rows]
    options = [{"name" : row[0]} for row in rows]
    cur.close()

    return




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

