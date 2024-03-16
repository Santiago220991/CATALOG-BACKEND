from app.src.exceptions import ProductRepositoryException

from app.src.repositories import ProductRepository

from .response import FilterProductResponse


class FilterProduct:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    def __call__(self, filter_by) -> FilterProductResponse:
        try:
            filtered_products = self.product_repository.filter(filter_by)
            response = FilterProductResponse(products=filtered_products)
            return response
        except ProductRepositoryException as error:
            raise error
