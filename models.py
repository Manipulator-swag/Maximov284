from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship


class material_type(Base):
    __tablename__ = "material_type"
    id = Column(Integer, primary_key=True)
    material_type = Column(String)
    loss_percent = Column(DECIMAL)


    products = relationship('products', back_populates='material')


class product_types(Base):
    __tablename__ = "product_types"
    id = Column(Integer, primary_key=True)
    product_type = Column(String)
    product_koeficent = Column(DECIMAL)


    products = relationship('products', back_populates='product_type_id')


class workshop(Base):
    __tablename__ = "workshop"
    id = Column(Integer, primary_key=True)
    workshop_name = Column(String)
    workshop_type = Column(String)
    population = Column(Integer)

    product_workshops = relationship('product_workshops', back_populates='workshop')


class product_workshops(Base):
    __tablename__ = "product_workshops"
    id = Column(Integer, primary_key=True)
    product_name = Column(Integer, ForeignKey('products.id'), nullable=False)
    workshop_name = Column(Integer, ForeignKey('workshop.id'), nullable=False)
    making_time = Column(DECIMAL)

    product = relationship('products', back_populates='product_workshops')
    workshop = relationship('workshop', back_populates='product_workshops')


class products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product_type = Column(Integer, ForeignKey("product_types.id"), nullable=False)
    product_name = Column(String)
    articul = Column(Integer)
    min_cost_for_partner = Column(DECIMAL)
    main_material= Column(Integer, ForeignKey("material_type.id"), nullable=False)

    product_type_id = relationship('product_types', back_populates='products')
    material = relationship('material_type', back_populates='products')
    product_workshops = relationship('product_workshops', back_populates='product')


