import pytest
from unittest.mock import patch

from app.src.exceptions import ProductRepositoryException
from app.src.use_cases.product.filter.response import FilterProductResponse
from app.src.use_cases.product.filter.use_case import FilterProduct


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
