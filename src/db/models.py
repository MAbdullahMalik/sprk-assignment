from sqlalchemy import Column, Integer, String, DateTime, JSON
from db import Base, engine


class Product(Base):
    __tablename__ = "products"

    amount = Column(Integer)
    bbd = Column(DateTime)
    comment = Column(String)
    amount_multiplier = Column(Integer)
    code = Column(String, primary_key=True, index=True)
    description = Column(String)
    id = Column(Integer)
    type = Column(String, primary_key=True)
    trade_item_unit_descriptor = Column(String)
    trade_item_unit_descriptor_name = Column(String)
    related_products = Column(JSON)
    net_weight = Column(JSON)
    gross_weight = Column(JSON)
    hierarchies = Column(JSON)
    vat = Column(JSON)


Base.metadata.create_all(engine)
