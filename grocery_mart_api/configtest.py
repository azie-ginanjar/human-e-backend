# SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
SQLALCHEMY_DATABASE_URI = "postgresql:///grocery_mart_api_test" #  using this because ARRAY type is not supp on sqlite
TESTING = True
ENV = "test"