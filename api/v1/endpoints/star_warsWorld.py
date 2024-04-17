from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.starWars_model import StarWarsWorldModel
from schemas.StarWarsWorlsSchema import StarWarsWorlsSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=StarWarsWorlsSchema)
async def post_mundos(mundo: StarWarsWorlsSchema, db: AsyncSession=Depends(get_session)):
    novo_mundo = StarWarsWorldModel(nome=mundo.nome, descricao=mundo.descricao)
    db.add(novo_mundo)
    await db.commit()
    
    return novo_mundo

@router.get("/", response_model=List[StarWarsWorlsSchema])
async def get_mundos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(StarWarsWorldModel)
        result = await session.execute(query)
        mundos: List[StarWarsWorldModel] = result.scalars().all()
        
        return mundos
    
@router.get("/{mundo_id}", response_model=StarWarsWorlsSchema, status_code=status.HTTP_200_OK)
async def get_mundo(mundo_id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(StarWarsWorldModel).filter(StarWarsWorldModel.id == mundo_id)
        result = await session.execute(query)
        mundo = result.scalar_one_or_none()
        
        if mundo:
            return mundo
        else:
            raise HTTPException(detail="Mundo não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
        
@router.put("/{mundo_id}", response_class=StarWarsWorlsSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_mundo(mundo_id: int, mundo:StarWarsWorlsSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(StarWarsWorldModel).filter(StarWarsWorldModel.id == mundo_id)
        result = await session.execute(query)
        mundo_up = result.scalar_one_or_none()
        
        if mundo_up:
            mundo_up.nome = mundo.nome
            mundo_up.descricao = mundo.descricao
                    
            await session.commit()
            
            return mundo_up
        
        else: 
            raise HTTPException(detail="Mundo não encontrado", status_code=status.HTTP_404_NOT_FOUND) 
        

@router.delete("/{mundo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mundo(mundo_id: int,  db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(StarWarsWorldModel).filter(StarWarsWorldModel.id == mundo_id)
        result = await session.execute(query)
        mundo_del = result.scalar_one_or_none()        
        
        if mundo_del:
            await session.delete(mundo_del)
            await session.commit
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="mundo não encontrado", status_code=status.HTTP_404_NOT_FOUND)         
