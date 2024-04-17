from typing import Optional
from pydantic import BaseModel as SCBaseModel

class StarWarsWorlsSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    
    class Config:
        orm_mode = True