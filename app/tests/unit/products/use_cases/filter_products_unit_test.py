import pytest
from unittest.mock import patch

from app.src.exceptions import ProductRepositoryException
from app.src.use_cases.product import FilterProduct, FilterProductResponse, UpdateProduct, UpdateProductResponse


def test_filter_products_success(mock_product_repository, fake_product_list):
    filter_by = "New"
    expected_filtered_products = fake_product_list
    mock_product_repository.filter.return_value = expected_filtered_products

    filter_product = FilterProduct(product_repository=mock_product_repository)

    response = filter_product(filter_by)

    assert mock_product_repository.filter.called_once_with(filter_by)
    assert response == FilterProductResponse(
        products=expected_filtered_products)


def test_filter_products_repository_exception(mocker, mock_product_repository):
    filter_by = "old"
    mock_product_repository.filter.side_effect = ProductRepositoryException(
        "filtering")

    filter_product = FilterProduct(product_repository=mock_product_repository)

    with pytest.raises(ProductRepositoryException) as exc_info:
        filter_product(filter_by)
    assert str(exc_info.value) == "Exception while executing filtering in Product"


def test_update_products_success(mock_product_repository, fake_product):
    expected_product = fake_product
    mock_product_repository.update.return_value = expected_product

    update_product = UpdateProduct(product_repository=mock_product_repository)

    response = update_product(expected_product.product_id, expected_product)

    assert mock_product_repository.filter.called_once_with(expected_product)
    assert response == UpdateProductResponse(user_id=expected_product.user_id,
                                             product_id= expected_product.product_id,
                                             name=expected_product.name,
                                             description=expected_product.description,
                                             price=expected_product.price,
                                             location=expected_product.location,
                                             status=expected_product.status,
                                             is_available=expected_product.is_available)
