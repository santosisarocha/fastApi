from core.configs import settings
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Stars_WarsModel(settings.DBBaseModel):
    __tablename__ = "personagens"
    
    id: int = Column(Integer(), primary_key=True, autoincrement=True)    
    nome: str = Column(String(30))
    descricao: str = Column(String(255))
    foto: str = Column(String(255))
    mundo_id = Column(Integer, ForeignKey('mundos.id'))
    mundo = relationship("StarWarsWorldModel", back_populates="personagens", lazy='joined')
    
class StarWarsWorldModel(settings.DBBaseModel):
    __tablename__ = "mundos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50))
    descricao = Column(String(255))    
    personagens = relationship("Stars_WarsModel", cascade="all,delete-orphan", back_populates="mundo",uselist=True, lazy='joined')
