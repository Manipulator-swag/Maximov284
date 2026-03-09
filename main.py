from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import text, Select
from fastapi.templating import Jinja2Templates

from Maximov284.models import ProductWorkshops



class MaterialAdd(Basemodel()):
    material_type: str
    loss_percent: float

class Materials(MaterialAdd):
    id: int


materials = []

@app.post("/materials_add")


async def Material_Add(
    material: Annotated[MaterialAdd, Depends()]):
    materials.append (material)
    return{"ok": True}

@app.get("/materials")
def getmatterials():
    return materials

workshops = []

@app.get("/workshops")
def getworkshops():
    return workshops

products = []

@app.get("/products")
def getproducts():
    return products