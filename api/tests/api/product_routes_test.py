from decimal import Decimal
from faker import Faker
from unittest.mock import MagicMock

from factories.use_cases.product import list_product_use_case, filter_product_use_case
from app.src.core.models._product import Product, ProductStatuses

fake = Faker()


def test_get_products_endpoint_success(app, client, mock_session_manager):
    mock_response = MagicMock()
    products = [Product(
        product_id=fake.uuid4(),
        user_id=fake.uuid4(),
        name=fake.word(),
        description=fake.sentence(),
        price=Decimal(fake.pyint(min_value=0, max_value=9999, step=1)),
        location=fake.address(),
        status=fake.random_element(elements=(
            ProductStatuses.NEW, ProductStatuses.USED, ProductStatuses.FOR_PARTS)),
        is_available=fake.boolean())]

    mock_response.products = products
    mock_use_case = MagicMock(return_value=mock_response)

    app.dependency_overrides[list_product_use_case] = lambda: mock_use_case

    response = client.get("/products/")

    assert response.status_code == 200

    expected_response = {
        "products": [{"product_id": products[0].product_id,
                      "user_id": products[0].user_id,
                      "name": products[0].name,
                      "description": products[0].description,
                      "price": str(products[0].price),
                      "location": products[0].location,
                      "status": products[0].status.value,
                      "is_available": products[0].is_available,
                      }]}
    assert response.json() == expected_response


def test_filter_products_endpoint_success(app, client, mock_session_manager):
    mock_response = MagicMock()
    products = [
        Product(
            product_id=fake.uuid4(),
            user_id=fake.uuid4(),
            name=fake.word(),
            description=fake.sentence(),
            price=Decimal(fake.pyint(min_value=0, max_value=9999, step=1)),
            location=fake.address(),
            status=ProductStatuses.NEW,
            is_available=fake.boolean()),
    ]

    mock_response.products = products
    mock_use_case = MagicMock(return_value=mock_response)

    app.dependency_overrides[filter_product_use_case] = lambda: mock_use_case
    filter_by = "New"
    response = client.get(f"/products/filter/{filter_by}")

    assert response.status_code == 200
    expected_response = {
        "products": [{"product_id": products[0].product_id,
                      "user_id": products[0].user_id,
                      "name": products[0].name,
                      "description": products[0].description,
                      "price": str(products[0].price),
                      "location": products[0].location,
                      "status": products[0].status.value,
                      "is_available": products[0].is_available,
                      }]}
    assert response.json() == expected_response
    mock_use_case.assert_called_once_with(filter_by)


def test_filter_products_endpoint_empty(app, client, mock_session_manager):
    mock_response = MagicMock()
    products = [
        Product(
            product_id=fake.uuid4(),
            user_id=fake.uuid4(),
            name=fake.word(),
            description=fake.sentence(),
            price=Decimal(fake.pyint(min_value=0, max_value=9999, step=1)),
            location=fake.address(),
            status=ProductStatuses.NEW,
            is_available=fake.boolean()),
    ]

    mock_response.products = []
    mock_use_case = MagicMock(return_value=mock_response)

    app.dependency_overrides[filter_product_use_case] = lambda: mock_use_case
    filter_by = "Used"
    response = client.get(f"/products/filter/{filter_by}")

    assert response.status_code == 200
    assert mock_use_case.call
    expected_response = {
        "products": []}
    assert response.json() == expected_response
    mock_use_case.assert_called_once_with(filter_by)
