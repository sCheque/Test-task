from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    on_sale: bool = False
    category_id: int


    class Config:
        orm_mode = True


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    on_sale: bool
    category: str


    class Config:
        orm_mode = True


class CategoryOut(BaseModel):
    id: int
    name: str


    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    id: int
    name: str


    class Config:
        orm_mode = True