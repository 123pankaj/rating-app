from rating_app.models import User, Product


def user_factory(i):
    return User(
        username="user{}".format(i),
        email="user{}@mail.com".format(i)
    )


def product_factory(i):
    return Product(
        name="product{}".format(i),
    )
