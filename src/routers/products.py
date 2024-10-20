from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status

from database import get_db
import models
import schemas

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def products(
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)

    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    if search:
        search_term = f"%{search}%"
        query = query.filter(models.Product.name.ilike(search_term))

    products = query.all()
    return products


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(name=product.name, 
                                 price=product.price, 
                                 on_sale=product.on_sale, 
                                 category_id=product.category_id)      
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found")
    return product


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if product.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not exist")
    product.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model = schemas.ProductOut)
def update_product(id: int, updated_post: schemas.ProductCreate, db: Session = Depends(get_db)):

    product_query = db.query(models.Post).filter(models.Product.id == id)
    product = product_query.first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not exist")
    product_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()

    return product_query.first()
