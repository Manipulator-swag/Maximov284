from fastapi import FastAPI, status, Depends, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db
from models import product_workshops, products, product_types, material_type, workshop
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from Schemas import add_product, update_product

templates = Jinja2Templates(directory='front')
app = FastAPI(title="main")

# Подключаем статические файлы
app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")

def get_hours_id(product_id: int, db):
    stmt = text('SELECT SUM(making_time) FROM "product_workshops" WHERE product_name = :product_id;')
    result = db.execute(stmt, {"product_id": product_id})
    return result.scalar()

@app.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    products_list = db.query(products).all()
    
    data = {"products": []}
    
    for product in products_list:
        data['products'].append({
            "product_type": product.product_type_id.product_type if product.product_type_id else None,
            "product_name": product.product_name,
            "articul": product.articul,
            "min_cost_for_partner": product.min_cost_for_partner,
            "making_time": get_hours_id(product.id, db),
            "main_material": product.material.material_type if product.material else None,
            "product_id": product.id
        })
    
    return templates.TemplateResponse(
        request=request,
        name="main.html",
        context={"data": data}
    )

@app.get("/products")
def get_product(db: Session = Depends(get_db)):
    products_list = db.query(products).all()
    
    data = {"products": []}
    
    for product in products_list:
        data['products'].append({
            "product_type": product.product_type_id.product_type if product.product_type_id else None,
            "product_name": product.product_name,
            "articul": product.articul,
            "min_cost_for_partner": product.min_cost_for_partner,
            "making_time": get_hours_id(product.id, db),
            "main_material": product.material.material_type if product.material else None,
            "product_id": product.id
        })
    return data

@app.get('/workshops/{product_id}')
def get_workshops(product_id:int, request:Request, db:Session=Depends(get_db)):
    workshops = db.query(product_workshops).filter(product_workshops.product_name == product_id).all()
    data = []

    for workshop in workshops:
        data.append({
            "make_time":workshop.making_time,
            "workshop_name":workshop.workshop.workshop_name if workshop.workshop else None,
            "population": workshop.workshop.population if workshop.workshop else None
        })   
    return templates.TemplateResponse(
        request=request,
        name='workshops.html',
        context={"data":data}
    )


@app.get('/all_workshops')
def get_all_workshops(request: Request, db: Session = Depends(get_db)):

    workshops_list = db.query(workshop).all()
    
    data = []
    for w in workshops_list:
        data.append({
            "workshop_name": w.workshop_name,
            "workshop_type": w.workshop_type,
            "population": w.population
        })
    
    return templates.TemplateResponse(
        request=request,
        name='all_workshops.html',
        context={"data": data}
    )

@app.get('/add_product')
def add_product_get(request: Request, db: Session = Depends(get_db)):
    product_types_data = db.query(product_types).all() 
    material_types_data = db.query(material_type).all()  

    product_types_list = [(pt.id, pt.product_type) for pt in product_types_data]
    material_types_list = [(mt.id, mt.material_type) for mt in material_types_data]
    
    return templates.TemplateResponse(
        request=request,
        name='add_products.html',
        context={
            "product_types": product_types_list, 
            "material_types": material_types_list
        }
    )


@app.post('/add_product')
def add_product_post(request: Request, product_request: add_product = Form(), db: Session = Depends(get_db)):
    try:
        product_new = products(
            product_type=product_request.product_type,
            product_name=product_request.product_name,
            articul=product_request.articul,
            min_cost_for_partner=product_request.min_partner_cost,
            main_material=product_request.main_material
        )
        db.add(product_new)
        db.commit()
        return RedirectResponse(url='/', status_code=303)
    except Exception as e:
        product_types_db = db.query(product_types).all()
        material_types_db = db.query(material_type).all()
        product_types = [(pt.id, pt.product_type) for pt in product_types_db]
        material_types = [(mt.id, mt.material_type) for mt in material_types_db]
        
        return templates.TemplateResponse(
            request=request,
            name='add_products.html',
            context={
                "product_types": product_types,
                "material_types": material_types,
                "error": str(e)
            }
        )

@app.get('/update_product/{product_id}')
def update_product_get(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(products).filter(products.id == product_id).first()
    
    if not product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'Товар с данным id не найден'}
        )

    product_types_data = db.query(product_types).all()
    material_types_data = db.query(material_type).all()

    product_types_list = [(pt.id, pt.product_type) for pt in product_types_data]
    material_types_list = [(mt.id, mt.material_type) for mt in material_types_data]
    
    return templates.TemplateResponse(
        request=request,
        name='update_product.html',
        context={
            "product_types": product_types_list, 
            "material_types": material_types_list,
            "product_id": product.id,
            "product_type_id": product.product_type,
            "material_id": product.main_material,
            "product_name": product.product_name,
            "articul": product.articul,
            "min_cost_for_partner": product.min_cost_for_partner  
        }
    )

@app.post('/update_product/{product_id}')
def update_product_post(product_id: int, request: Request, product_request: update_product = Form(), db: Session = Depends(get_db)):
    product = db.query(products).filter(products.id == product_id).first()
    
    if not product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'Товар с данным id не найден'}
        )
    
    try:
        product.product_type = product_request.product_type
        product.product_name = product_request.product_name
        product.articul = product_request.articul
        product.min_cost_for_partner = product_request.min_partner_cost
        product.main_material = product_request.main_material
        
        db.commit()
        return RedirectResponse(url='/', status_code=303)
    except Exception as e:
        product_types_db = db.query(product_types).all()
        material_types_db = db.query(material_type).all()
        product_types_list = [(pt.id, pt.product_type) for pt in product_types_db]
        material_types_list = [(mt.id, mt.material_type) for mt in material_types_db]
        
        return templates.TemplateResponse(
            request=request,
            name='update_product.html',
            context={
                "product_types": product_types_list,
                "material_types": material_types_list,
                "product_id": product_id,
                "product_type_id": product_request.product_type,
                "material_id": product_request.main_material,
                "product_name": product_request.product_name,
                "articul": product_request.articul,
                "min_cost_for_partner": product_request.min_partner_cost,
                "error": str(e)
            }
        )

@app.post('/delete_product/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        db.query(product_workshops).filter(product_workshops.product_name == product_id).delete()
        product = db.query(products).filter(products.id == product_id).first()
        
        if product:
            db.delete(product)
            db.commit()
            return RedirectResponse(url='/', status_code=303)
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Продукт не найден"}
            )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"message": f"Ошибка при удалении: {str(e)}"}
        )

@app.get('/delete_product/{product_id}')
def delete_product_get(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(products).filter(products.id == product_id).first()
    
    if not product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'Товар с данным id не найден'}
        )
    
    return templates.TemplateResponse(
        request=request,
        name='delete_product.html',
        context={
            "product_id": product.id,
            "product_name": product.product_name    
        }
    )
