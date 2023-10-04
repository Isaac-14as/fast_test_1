from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
)