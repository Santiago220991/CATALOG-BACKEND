from typing import Any, Optional

from app.src.core import Product
from app.src.repositories import ProductRepository
from app.src.exceptions import ProductNoneException, ProductRepositoryException, ProductBusinessException

from .response import UpdateProductResponse
from .request import UpdateProductRequest


class UpdateProduct:
  def __init__(self, product_repository: ProductRepository) -> None:
    self.product_repository = product_repository

  def __call__(self, product_id: str, request: UpdateProductRequest) -> Optional[UpdateProductResponse]:
    product = Product(**request._asdict())
    try:
      product_existing = self.product_repository.get_by_id(product_id)
      if product_existing:
        response: Optional[Product] = self.product_repository.update(product_id, product)
      if not product_existing:
        raise ProductNoneException()

      return UpdateProductResponse(**response._asdict())
    except ProductRepositoryException as e:
      raise ProductBusinessException(str(e))
