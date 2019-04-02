import factory.fuzzy
from pytest_factoryboy import register

from rating_app.models import Product


@register
class ProductFactory(factory.Factory):
    name = factory.Sequence(lambda n: 'product%d' % n)
    price = factory.fuzzy.FuzzyFloat(10.0, 50.0)

    class Meta:
        model = Product


def test_get_product(client, db, product):
    # test 404
    rep = client.get("/api/v1/products/100000")
    assert rep.status_code == 404

    db.session.add(product)
    db.session.commit()

    # test get_product
    rep = client.get('/api/v1/products/%d' % product.id)
    assert rep.status_code == 200

    data = rep.get_json()['product']
    assert data['name'] == product.name
    assert data['price'] == product.price


def test_put_product(client, db, product):
    # test 404
    rep = client.put("/api/v1/products/100000")
    assert rep.status_code == 404

    db.session.add(product)
    db.session.commit()

    data = {'name': 'updated'}

    # test update product
    rep = client.put(
        '/api/v1/products/%d' % product.id,
        json=data
    )
    assert rep.status_code == 200

    data = rep.get_json()['product']
    assert data['name'] == 'updated'
    assert data['price'] == product.price


def test_delete_product(client, db, product):
    # test 404
    rep = client.put("/api/v1/products/100000")
    assert rep.status_code == 404

    db.session.add(product)
    db.session.commit()

    # test get_product
    product_id = product.id
    rep = client.delete(
        '/api/v1/products/%d' % product_id
    )
    assert rep.status_code == 200
    assert db.session.query(Product).filter_by(id=product_id).first() is None


def test_create_product(client, db):
    # test bad data
    data = {
        'name': 'created'
    }
    rep = client.post(
        '/api/v1/products',
        json=data
    )
    assert rep.status_code == 422

    data['price'] = 30.0

    rep = client.post(
        '/api/v1/products',
        json=data
    )
    assert rep.status_code == 201

    data = rep.get_json()
    product = db.session.query(Product).filter_by(id=data['product']['id']).first()

    assert product.name == 'created'
    assert product.price == 30.0


def test_get_all_product(client, db, product_factory):
    products = product_factory.create_batch(30)

    db.session.add_all(products)
    db.session.commit()

    rep = client.get('/api/v1/products')
    assert rep.status_code == 200

    results = rep.get_json()
    for product in products:
        assert any(u['id'] == product.id for u in results['results'])
