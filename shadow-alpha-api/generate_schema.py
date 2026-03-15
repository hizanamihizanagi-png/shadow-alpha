import sys
import os
import types

# Mock email_validator to prevent Pydantic from crashing on EmailStr
sys.modules['email_validator'] = types.ModuleType('email_validator')

# Ensure the parent directory is in the PYTHONPATH so 'app' can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from app.db.base import Base
# Import all models so they register with Base.metadata
from app.models import user, position, order, tontine, vault, shield, subscription, loan, gratitude, position_loan, wealth_engine

def get_create_table_string(table):
    return str(CreateTable(table.__table__).compile(dialect=postgresql.dialect()))

if __name__ == "__main__":
    print("-- PostgreSQL Schema generated from SQLAlchemy models\n")
    for table in Base.__subclasses__():
        print(get_create_table_string(table))
        print(";")
