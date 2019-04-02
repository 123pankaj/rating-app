import click
from flask.cli import FlaskGroup

from rating_app.app import create_app


def create_rating_app(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_rating_app)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create sample users and products and orders
    """
    from rating_app.extensions import db
    from rating_app.models import User, Product, Order
    click.echo("create database")
    db.create_all()
    click.echo("done")

    click.echo("create user")
    user1 = User(
        username='user1',
        email='user1@mail.com',
    )
    product1 = Product(
        name='Table',
        price=20.0
    )
    product2 = Product(
        name='Chair',
        price=15.0
    )
    product3 = Product(
        name='Lamp',
        price=10.0
    )
    order = Order(
        user=user1,
        product=product1,
        quantity=2,
    )
    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(user1)
    db.session.add(order)
    db.session.commit()


if __name__ == "__main__":
    cli()
