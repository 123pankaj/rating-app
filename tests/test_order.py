import factory.fuzzy
from pytest_factoryboy import register

from rating_app.models import Product, User, Order


@register
class UserFactory(factory.Factory):
    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@mail.com' % n)

    class Meta:
        model = User


@register
class ProductFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'product%d' % n)
    price = factory.fuzzy.FuzzyFloat(10.0, 50.0)

    class Meta:
        model = Product


@register
class OrderFactory(factory.Factory):
    quantity = factory.fuzzy.FuzzyInteger(0, 5)
    ratings = factory.fuzzy.FuzzyInteger(0, 5)

    class Meta:
        model = Order


def test_get_order(client, db, order):
    # test 404
    rep = client.get("/api/v1/orders/100000")
    assert rep.status_code == 404

    db.session.add(order)
    db.session.commit()

    # test get_order
    rep = client.get('/api/v1/orders/%d' % order.id)
    assert rep.status_code == 200

    data = rep.get_json()['order']
    assert data['quantity'] == order.quantity
    assert data['ratings'] == order.ratings


def test_put_order(client, db, order):
    # test 404
    rep = client.put("/api/v1/orders/100000")
    assert rep.status_code == 404

    db.session.add(order)
    db.session.commit()

    data = {'ratings': 1}

    # test update order
    rep = client.put(
        '/api/v1/orders/%d' % order.id,
        json=data
    )
    assert rep.status_code == 200

    data = rep.get_json()['order']
    assert data['ratings'] == 1


def test_delete_order(client, db, order):
    # test 404
    rep = client.put("/api/v1/orders/100000")
    assert rep.status_code == 404

    db.session.add(order)
    db.session.commit()

    # test get_order
    order_id = order.id
    rep = client.delete(
        '/api/v1/orders/%d' % order_id
    )
    assert rep.status_code == 200
    assert db.session.query(Order).filter_by(id=order_id).first() is None


def test_create_order(client, db):
    # test bad data
    data = {
        'quantity': 2,
    }
    rep = client.post(
        '/api/v1/orders',
        json=data
    )
    assert rep.status_code == 422

    data['user_id'] = 1
    data['product_id'] = 1
    data['quantity'] = 2

    rep = client.post(
        '/api/v1/orders',
        json=data
    )
    assert rep.status_code == 201

    data = rep.get_json()
    order = db.session.query(Order).filter_by(id=data['order']['id']).first()

    assert order.quantity == 2


def test_get_all_order(client, db, order_factory):
    orders = order_factory.create_batch(30)

    db.session.add_all(orders)
    db.session.commit()

    rep = client.get('/api/v1/orders')
    assert rep.status_code == 200

    results = rep.get_json()
    for order in orders:
        assert any(u['id'] == order.id for u in results['results'])
