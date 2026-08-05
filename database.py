import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.environ.get("MYSQL_USER", "avnadmin"),
    password=os.environ.get("MYSQL_PASSWORD", "AVNS_kLgxK_HL0S6OZOQ3mYx"),
    host=os.environ.get("MYSQL_HOST", "fastapi-mysql-fastapi-project-goat.a.aivencloud.com"),
    port=int(os.environ.get("MYSQL_PORT", 13591)),
    database=os.environ.get("MYSQL_DATABASE", "defaultdb"),
    query={"charset": "utf8mb4"},
)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "connect_timeout": 10,
        "ssl": {}, # Required for Aiven
    },
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
