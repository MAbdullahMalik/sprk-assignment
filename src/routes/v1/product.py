from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from db import get_database
from schemas.models import Product
from controllers.products_controller import ProductController

router = APIRouter()


@router.post("/")
def store(products: Product, response: Response, db: Session = Depends(get_database)):
    try:
        response.status_code = 207
        return ProductController().store_product(db=db, products=products)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))  # todo


@router.get("/{code}", status_code=status.HTTP_200_OK)
def get_one(code, db: Session = Depends(get_database)):
    return ProductController().get_one(db=db, code=code)


@router.get("/", status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_database)):
    return ProductController().get_all(db=db)

