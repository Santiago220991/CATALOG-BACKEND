from typing import List, NamedTuple

from pydantic import BaseModel

from ....core.models._product import Product


class FilterProductResponse(BaseModel):
    products: List[Product]
