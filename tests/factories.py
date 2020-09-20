from grocery_mart_api.models import User


def user_factory(i):
    return User(
        username="user{}".format(i),
        email="user{}@mail.com".format(i)
    )
