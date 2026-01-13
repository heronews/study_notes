from sqlalchemy import create_engine, MetaData
from .settings import app_settings

sql_engine = create_engine(app_settings.db_url, echo=True)
sql_metadata = MetaData()
