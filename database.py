from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALHEMY_DATABASE_URL = "mysql+mysqldb://root:N6M2v2bOHxxRTfYtSbTpZTWNvoO6OlRg@192.168.1.218:3306/fastapi-ca"
engine = create_engine(SQLALHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()