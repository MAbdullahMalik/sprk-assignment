from typing import List
from sqlalchemy.orm import Session
from db import Product
import json
from utils.text_utils import remove_leading_zeros, parse_unicode_characters


class ProductController:
    def store_product(self, db: Session, products: Product):
        success = []
        failed = []

        # Duplicate products needs to merge the amounts
        self.merge_duplicate(products)

        codes = self.get_codes(products)

        # fetch existing products  -- optimization
        db_records = db.query(Product).filter(Product.code.in_(codes)).all()

        # updating records
        for item in products.amounts:
            self.normalize_data(item)

            # update case
            status = self.update_existing_product(item, db_records)
            if status is False:
                # new case
                if item.item.type is None:
                    failed.append({"code": item.item.code, "type": item.item.type, "message": "No type found"})
                else:
                    self.add_product(db, item)
                    success.append({"code": item.item.code, "type": item.item.type, "message": "Added", "amount": item.amount})
            else:
                success.append({"code": item.item.code, "type": item.item.type, "message": "Updated", "amount": item.amount})

        db.commit()
        return {"status_code": 207, "response": [{"failed": failed}, {"success": success}]}

    def merge_duplicate(self, products: Product):
        products_dict = {}
        for item in products.amounts:
            # without item type we can't proceed
            if item.item.type is None:
                continue
            # as we identify products via [code & type]
            key = str(item.item.code) + '_' + str(item.item.type)
            if key in products_dict:
                # duplicated product found so adding the amount
                item.amount = item.amount + self.get_amount_and_delete_previous(products, item.item.code, item.item.type)
            else:
                products_dict[key] = item

    def normalize_data(self, item: Product):
        item.item.code = remove_leading_zeros(item.item.code)
        item.item.description = parse_unicode_characters(item.item.description)
        item.comment = parse_unicode_characters(item.comment)
        self.transform_fields(item)

    def get_amount_and_delete_previous(self, products: Product, code: str, type: str):
        count = 0
        for item in products.amounts:
            if item.item.code == code and item.item.type == type:
                amount = item.amount
                del products.amounts[count]
                return amount
            count = count + 1
        return 0

    def transform_fields(self, item: Product):
        if item.item.trade_item_descriptor is not None:
            item.item.trade_item_unit_descriptor = item.item.trade_item_descriptor

    def get_codes(self, products: Product):
        codes = []
        for item in products.amounts:
            # because database don't contains any leading zeros
            codes.append(remove_leading_zeros(item.item.code))
        return codes

    def update_existing_product(self, item, db_records):
        for row in db_records:
            if row.code == item.item.code and row.type == item.item.type:
                row.amount = row.amount + item.amount
                item.amount = row.amount
                return True
        return False

    def add_product(self, db: Session, item: Product):
        db_product = Product(
            amount=item.amount,
            bbd=item.bbd,
            comment=item.comment,
            amount_multiplier=item.item.amount_multiplier,
            code=item.item.code,
            description=item.item.description,
            id=item.item.id,
            type=item.item.type,
            net_weight=json.dumps(item.item.net_weight),
            trade_item_unit_descriptor=item.item.trade_item_unit_descriptor,
            trade_item_unit_descriptor_name=item.item.trade_item_unit_descriptor_name,
        )
        db.add(db_product)

    def get_one(self, db: Session, code: str):
        result = db.query(Product).filter_by(code=code).all()
        self.transform_product(result)
        return result

    def get_all(self, db: Session):
        result = db.query(Product).all()
        self.transform_product(result)
        return result

    def transform_product(self, products: List[Product]):
        for item in products:
            if item.net_weight is not None:
                item.net_weight = json.loads(item.net_weight)
            else:
                del item.net_weight
            if item.gross_weight is not None:
                item.gross_weight = json.loads(item.gross_weight)
            else:
                del item.gross_weight
            if item.hierarchies is not None:
                item.hierarchies = json.loads(item.hierarchies)
            else:
                del item.hierarchies
            if item.vat is not None:
                item.vat = json.loads(item.vat)
            else:
                del item.vat
