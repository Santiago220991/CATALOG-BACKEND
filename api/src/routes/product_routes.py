from typing import List

from fastapi import APIRouter, Depends

from app.src.use_cases import (
    ListProducts,
    ListProductResponse,
    FindProductById,
    FindProductByIdResponse,
    FindProductByIdRequest,
    CreateProduct,
    CreateProductResponse,
    CreateProductRequest,
    FilterProduct,
    UpdateProduct,
    UpdateProductRequest,
    UpdateProductResponse,
    DeleteProductResponse,
    DeleteProductRequest,
    DeleteProduct
)
from ..dtos import (
    ProductBase,
    ListProductResponseDto,
    CreateProductRequestDto,
    CreateProductResponseDto,
    FindProductByIdResponseDto,
    FilterProductResponseDto,
    UpdateProductResponseDto,
    UpdateProductRequestDto,
)
from factories.use_cases import (
    list_product_use_case,
    find_product_by_id_use_case,
    create_product_use_case,
    filter_product_use_case,
    update_product_use_case,
    delete_product_use_case,
)
from app.src.core.models import Product

product_router = APIRouter(prefix="/products")


@product_router.get("/", response_model=ListProductResponseDto)
async def get_products(
    use_case: ListProducts = Depends(list_product_use_case)
) -> ListProductResponse:
    response_list = use_case()
    response = [{**product._asdict(), "status": str(product.status.value)}
                for product in response_list.products]
    response_dto: ListProductResponseDto = ListProductResponseDto(
        products=[ProductBase(**product) for product in response]
    )
    return response_dto


@product_router.get("/{product_id}", response_model=FindProductByIdResponseDto)
async def get_product_by_id(
    product_id: str,
    use_case: FindProductById = Depends(find_product_by_id_use_case)
) -> FindProductByIdResponse:
    response = use_case(FindProductByIdRequest(product_id=product_id))
    response_dto: FindProductByIdResponseDto = FindProductByIdResponseDto(
        **response._asdict())
    return response_dto


@product_router.post("/", response_model=CreateProductResponseDto | str)
async def create_product(
    request: CreateProductRequestDto,
    use_case: CreateProduct = Depends(create_product_use_case)
) -> CreateProductResponse:
    if request.status not in ["New", "Used", "For parts"]:
        return "Not a valid status value (New, Used, For parts)"

    response = use_case(CreateProductRequest(
        product_id=request.product_id,
        user_id=request.user_id,
        name=request.name,
        description=request.description,
        price=request.price,
        location=request.location,
        status=request.status,
        is_available=request.is_available
    ))
    response_dto: CreateProductResponseDto = CreateProductResponseDto(
        **response._asdict())
    return response_dto


@product_router.get("/filter/{filter_by}", response_model=ListProductResponseDto | str)
async def filter_product(
    filter_by: str,
    use_case: FilterProduct = Depends(filter_product_use_case),
) -> ListProductResponse:
    if filter_by not in ["New", "Used", "For parts"]:
        return "Not a valid filter value (New, Used, For parts)"

    response_list = use_case(filter_by)
    response = [{**product._asdict(), "status": str(product.status.value)}
                for product in response_list.products]
    response_dto: FilterProductResponseDto = FilterProductResponseDto(
        products=[ProductBase(**product) for product in response]
    )
    return response_dto


@product_router.put("/{product_id}",  operation_id="update_product", response_model=UpdateProductResponseDto | str)
async def update_product(
    product_id: str,
    request: UpdateProductRequestDto,
    use_case: UpdateProduct = Depends(update_product_use_case)
) -> UpdateProductResponse:
    if request.status not in ["New", "Used", "For parts"]:
        return "Not a valid status value (New, Used, For parts)"
    response = use_case(product_id, UpdateProductRequest(
        product_id=product_id,
        user_id=request.user_id,
        name=request.name,
        description=request.description,
        price=request.price,
        location=request.location,
        status=request.status,
        is_available=request.is_available
    ))
    response_dto: UpdateProductResponseDto = UpdateProductResponseDto(
        **response._asdict())
    return response_dto


@product_router.delete("/{product_id}", response_model=str)
async def delete_product(
    product_id: str,
    use_case: DeleteProduct = Depends(delete_product_use_case)
) -> DeleteProductResponse:
    try:
        response = use_case(DeleteProductRequest(product_id=product_id))
        return f"The product with id {response} was deleted."
    except Exception as error:
        return str(error)
