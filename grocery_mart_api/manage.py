import click
from flask.cli import FlaskGroup

from grocery_mart_api.app import create_app


def create_grocery_mart_api(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_grocery_mart_api)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from grocery_mart_api.extensions import db
    from grocery_mart_api.models import User
    click.echo("create database")
    db.create_all()
    click.echo("done")

    click.echo("create user")
    user = User(
        username='admin',
        business_name="admin_business",
        email='admin@mail.com',
        password='admin',
        role="admin"
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
