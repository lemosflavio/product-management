from pydantic import BaseModel, Field


class DeleteProductCommand(BaseModel):
    id_: str = Field(alias='id')
