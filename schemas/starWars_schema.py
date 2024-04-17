from typing import Optional
from pydantic import BaseModel as SCBaseModel

class Star_WarsSchema(SCBaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    foto: str
    mundo_id: Optional[int]
    
    class Config:
        orm_mode = True
        
