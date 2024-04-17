from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.starWars_model import Stars_WarsModel
from schemas.starWars_schema import Star_WarsSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Star_WarsSchema)
async def post_personagens(personagem: Star_WarsSchema, db: AsyncSession=Depends(get_session)):
    novo_personagem = Stars_WarsModel(nome=personagem.nome, descricao=personagem.descricao, foto=personagem.foto)
    db.add(novo_personagem)
    await db.commit()
    
    return novo_personagem

@router.get("/", response_model=List[Star_WarsSchema])
async def get_personagens(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Stars_WarsModel)
        result = await session.execute(query)
        personagens: List[Stars_WarsModel] = result.scalars().all()
        
        return personagens
    
@router.get("/{personagem_id}", response_model=Star_WarsSchema, status_code=status.HTTP_200_OK)
async def get_personagem(personagem_id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Stars_WarsModel).filter(Stars_WarsModel.id == personagem_id)
        result = await session.execute(query)
        personagem = result.scalar_one_or_none()
        
        if personagem:
            return personagem
        else:
            raise HTTPException(detail="Personagem não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
        
@router.put("/{personagem_id}", response_class=Star_WarsSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_personagem(personagem_id: int, personagem:Star_WarsSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Stars_WarsModel).filter(Stars_WarsModel.id == personagem_id)
        result = await session.execute(query)
        personagem_up = result.scalar_one_or_none()
        
        if personagem_up:
            personagem_up.nome = personagem.nome
            personagem_up.descricao = personagem.descricao
            personagem_up.foto = personagem.foto
            
            await session.commit()
            
            return personagem_up
        
        else: 
            raise HTTPException(detail="Personagem não encontrado", status_code=status.HTTP_404_NOT_FOUND) 
        

@router.delete("/{personagem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_personagem(personagem_id: int,  db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Stars_WarsModel).filter(Stars_WarsModel.id == personagem_id)
        result = await session.execute(query)
        personagem_del = result.scalar_one_or_none()        
        
        if personagem_del:
            await session.delete(personagem_del)
            await session.commit
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Personagem não encontrado", status_code=status.HTTP_404_NOT_FOUND)         
