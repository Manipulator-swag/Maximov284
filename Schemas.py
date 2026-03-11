from  pydantic import BaseModel,PositiveInt
from decimal import Decimal



class add_product(BaseModel):
    product_type: int
    product_name: str
    articul: int
    min_partner_cost: Decimal
    main_material: int


class update_product(BaseModel):
    product_type: int
    product_name: str
    articul: int
    min_partner_cost: Decimal
    main_material: int