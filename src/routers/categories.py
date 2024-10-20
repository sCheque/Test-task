from typing import List
from fastapi import APIRouter, Depends, status
import models, schemas
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
  
    new_category = models.Category(id=category.id, name=category.name)      
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category



