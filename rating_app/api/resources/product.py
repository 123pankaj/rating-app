from flask import request
from flask_restful import Resource

from rating_app.commons.pagination import paginate
from rating_app.extensions import ma, db
from rating_app.models import Product


class ProductSchema(ma.ModelSchema):
    avg_ratings = ma.Float(dump_only=True, default=0.0)

    class Meta:
        model = Product
        sqla_session = db.session
        exclude = ["orders", ]


class ProductResource(Resource):
    """Single object resource
    """

    def get(self, product_id):
        schema = ProductSchema()
        user = Product.query.get_or_404(product_id)
        return {"product": schema.dump(user).data}

    def put(self, product_id):
        schema = ProductSchema(partial=True)
        product = Product.query.get_or_404(product_id)
        product, errors = schema.load(request.json, instance=product)
        if errors:
            return errors, 422

        return {"msg": "product updated", "product": schema.dump(product).data}

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()

        return {"msg": "product deleted"}


class ProductList(Resource):
    """Creation and get_all
    """

    def get(self):
        schema = ProductSchema(many=True)
        query = Product.query
        return paginate(query, schema)

    def post(self):
        schema = ProductSchema()
        product, errors = schema.load(request.json)
        if errors:
            return errors, 422

        db.session.add(product)
        db.session.commit()

        return {"msg": "product created", "product": schema.dump(product).data}, 201
