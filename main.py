from typing import Annotated, Optional
from fastapi import Depends, FastAPI
from pyndatic import Basemodel
app = FastAPI()
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