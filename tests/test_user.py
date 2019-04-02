import factory
from pytest_factoryboy import register

from rating_app.models import User


@register
class UserFactory(factory.Factory):
    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@mail.com' % n)

    class Meta:
        model = User


def test_get_user(client, db, user):
    # test 404
    rep = client.get("/api/v1/users/100000")
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    rep = client.get('/api/v1/users/%d' % user.id)
    assert rep.status_code == 200

    data = rep.get_json()['user']
    assert data['username'] == user.username
    assert data['email'] == user.email


def test_put_user(client, db, user):
    # test 404
    rep = client.put("/api/v1/users/100000")
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    data = {'username': 'updated'}

    # test update user
    rep = client.put(
        '/api/v1/users/%d' % user.id,
        json=data
    )
    assert rep.status_code == 200

    data = rep.get_json()['user']
    assert data['username'] == 'updated'
    assert data['email'] == user.email


def test_delete_user(client, db, user):
    # test 404
    rep = client.put("/api/v1/users/100000")
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    user_id = user.id
    rep = client.delete(
        '/api/v1/users/%d' % user_id
    )
    assert rep.status_code == 200
    assert db.session.query(User).filter_by(id=user_id).first() is None


def test_create_user(client, db):
    # test bad data
    data = {
        'username': 'created'
    }
    rep = client.post(
        '/api/v1/users',
        json=data
    )
    assert rep.status_code == 422

    data['email'] = 'create@mail.com'

    rep = client.post(
        '/api/v1/users',
        json=data
    )
    assert rep.status_code == 201

    data = rep.get_json()
    user = db.session.query(User).filter_by(id=data['user']['id']).first()

    assert user.username == 'created'
    assert user.email == 'create@mail.com'


def test_get_all_user(client, db, user_factory):
    users = user_factory.create_batch(30)

    db.session.add_all(users)
    db.session.commit()

    rep = client.get('/api/v1/users')
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u['id'] == user.id for u in results['results'])
