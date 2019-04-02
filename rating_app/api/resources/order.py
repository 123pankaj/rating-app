from flask import request
from flask_restful import Resource

from rating_app.commons.pagination import paginate
from rating_app.extensions import ma, db
from rating_app.models import Order


class OrderSchema(ma.ModelSchema):
    user_id = ma.Integer(load_only=True, required=True)
    product_id = ma.Integer(load_only=True, required=True)

    class Meta:
        model = Order
        sqla_session = db.session


class OrderResource(Resource):
    """Single object resource
    """

    def get(self, order_id):
        schema = OrderSchema()
        user = Order.query.get_or_404(order_id)
        return {"order": schema.dump(user).data}

    def put(self, order_id):
        schema = OrderSchema(partial=True)
        order = Order.query.get_or_404(order_id)
        order, errors = schema.load(request.json, instance=order)
        if errors:
            return errors, 422

        db.session.add(order)
        db.session.commit()
        if errors:
            return errors, 422

        return {"msg": "order updated", "order": schema.dump(order).data}

    def delete(self, order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()

        return {"msg": "order deleted"}


class OrderList(Resource):
    """Creation and get_all
    """

    def get(self):
        schema = OrderSchema(many=True)
        query = Order.query
        return paginate(query, schema)

    def post(self):
        schema = OrderSchema()
        order, errors = schema.load(request.json)
        if errors:
            return errors, 422

        db.session.add(order)
        db.session.commit()

        return {"msg": "order created", "order": schema.dump(order).data}, 201
