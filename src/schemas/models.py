from typing import Optional, List, Union
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class RelatedProduct(BaseModel):
    gtin: str = Field(None)
    trade_item_unit_descriptor: str = Field(None)


class Item(BaseModel):
    amount_multiplier: Optional[int]
    brand: str = Field(None)
    categ_id: Optional[int]
    category_id: str = Field(None)
    code: str
    description: str = Field(None)
    edeka_article_number: Optional[str]
    gross_weight: Optional[int]
    id: Optional[str]
    net_weight: Union[int, dict, None]
    gross_weight: Union[int, dict, None]
    hierarchies: Union[dict, None]
    vat: Union[dict, None]
    notes: Union[bool, str, None]
    packaging: str = Field(None)
    related_products: Optional[List[RelatedProduct]]
    requires_best_before_date: Optional[bool]
    requires_meat_info: Optional[bool]
    trade_item_unit_descriptor: str = Field(None)
    trade_item_descriptor: str = Field(None)
    trade_item_unit_descriptor_name: str = Field(None)
    type: Union[str, None]
    unit_name: str = Field(None)
    validation_status: str = Field(None)


class Amount(BaseModel):
    amount: int
    bbd: str = Field(None)
    comment: str = Field(None)
    country_of_disassembly: str = Field(None)
    country_of_rearing: str = Field(None)
    country_of_slaughter: str = Field(None)
    cutting_plant_registration : str = Field(None)
    item: Item
    lot_number: str = Field(None)
    slaughterhouse_registration: str = Field(None)


class Product(BaseModel):
    amounts: List[Amount]
    session_end_time: Optional[str]
    session_id: Optional[int]
    session_start_time: Optional[str]
    supplier_id: Optional[str]
    user_id: Optional[str]
