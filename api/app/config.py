from pydantic import BaseSettings, Field


class ApiConfig(BaseSettings):
    NAME: str = Field(default='product_api')
    HOST: str = Field(default='0.0.0.0')
    PORT: int = Field(default=8000)


class DBConfig(BaseSettings):
    URI: str = Field(default='mongodb://0.0.0.0:27017/')
    COLLECTION_NAME: str = Field(default='product')
    DATABASE_NAME: str = Field(default='product_management')


API_CONFIG = ApiConfig()
DATABASE_CONFIG = DBConfig()
