import uuid
from fastapi import FastAPI, Body, status, Depends, Request
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import product_workshops, products, product_types, material_type
from fastapi.templating import Jinja2Templates
from sqlalchemy import text, Select

templates = Jinja2Templates(directory='front')

app = FastAPI(title="main")

@app.get('/')
def main():
    return {"message":"hello"}

@app.get("/products")
def get_product(db: Session = Depends(get_db)):
    products_list = db.query(products).all()
    
    data = {"products": []}
    
    for product in products_list:
        data['products'].append({
            "product_type": product.product_type_id.product_type,  # Access through relationship
            "product_name": product.product_name,
            "articul": product.articul,
            "min_cost_for_partner": product.min_cost_for_partner,
            "hours": get_hours_id(product.id, db),
            "base_material": product.material.material_type,  # Access through relationship
            "product_id": product.id
        })
    return data

def get_hours_id(product_id: int, db):
    stmt = text('SELECT SUM(making_time) FROM "product_workshops" WHERE product_name = :product_id;')
    result = db.execute(stmt, {"product_id": product_id})
    return result.scalar()

# @app.post('/update_product/{product_id}', status_code=201)
# def update_product_post(product_id:int, product_request:UpdateProduct=Form(), db:Session=Depends(get_db)):
# product = db.query(products).where(products.id == product_request.id).first()
# if not product:
#     return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=[])
# try:
#     product.prouct_type = product_request.product_type
#     product.product_name = product_request.product_name,
#     product.articul = product_request.articul
#     product.base_material = product_request.base_material
#     product.min_partner_cost = product_request.min_partner_cost
#     db.commit()
#     db.refresh(product)
#     return JSONResponse(status_code=status.HTTP_201_CREATED,content=[])
# except Exception as e:
#     return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=[])


@app.get('/workshops/{product_id}')
def get_workshops(product_id:int,request:Request, db:Session=Depends(get_db)):
    workshops = db.query(product_workshops).all()
    data = []

    for workshop in workshops:
        data.append({
            "make_time":workshop.making_time,
            "workshop_name":workshop.workshop.workshop_name,
            "population": workshop.workshop.population
        })   
    return templates.TemplateResponse(
        request=request,
        name='workshops.html',
        context={"data":data}
    )



