from flask import Blueprint
from flask_restful import Api

from rating_app.api.resources import UserResource, UserList, ProductResource, ProductList, OrderResource, OrderList

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(ProductResource, '/products/<int:product_id>')
api.add_resource(ProductList, '/products')
api.add_resource(OrderResource, '/orders/<int:order_id>')
api.add_resource(OrderList, '/orders')
