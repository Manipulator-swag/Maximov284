from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey,DECIMAL
from sqlalchemy.orm import relationship

class material_type(Base):
    __tableName__="material_type"
    id = Column(Integer, primary_key = True)
    material_type = Column(String)
    loss_percent = Column(DECIMAL)

    base_materials = relationship('products', back_populates='main_material')


class product_types(Base):
    __tableName__= "product_types"
    id = Column(Integer, primary_key = True)
    product_type = Column(String)
    product_koeficent = Column(DECIMAL)
    
    products = relationship('products', back_populates='product_types')


class workshop(Base):
    __tableName__ = "workshop"
    id = Column(Integer, primary_key = True)
    workshop_name = Column(String)
    workshop_type = Column(String)
    population = Column(Integer)


    workshop_name  = relationship("workshop_name", back_populates = "workshop")


class product_workshops(Base):
    __tableName__ = "product_workshops"
    id = Column(Integer, primary_key = True)
    product_name = Column()
    product_type = Column()
    making_time = Column(DECIMAL)



class products(Base):
    __tablename__="products"
    id = Column(Integer, primary_key = True)
    prouct_type =Column(Integer, ForeignKey("product_types.id"))
    product_name= Column(String)
    articul=Column(Integer)
    min_partner_cost=Column(DECIMAL)
    base_material = Column(Integer,ForeignKey("material_type.id"))
   
    product_types = relationship('ProductsType', back_populates='products')
    materials = relationship('material_type', back_populates='base_materials')
    
    product_workshops = relationship("product_workshops", back_populates="products")

