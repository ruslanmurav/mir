from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import AuthUser
from src.database import get_async_session
from src.questionnaire import crud
from src.questionnaire.schemas import (
    CreateUserQuestionnaireSchema,
    ResponseUserQuestionnaireSchema,
)

router = APIRouter(
    prefix="/questionnaire",
    tags=["Questionnaire"],
)


@router.post(
    "",
    response_model=ResponseUserQuestionnaireSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_questionnaire(
    user_profile: CreateUserQuestionnaireSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return await crud.create_questionnaire(user_profile, session)




@router.get(
    "/list",
    response_model=list[ResponseUserQuestionnaireSchema],
    status_code=status.HTTP_200_OK,
)
async def get_list_questionnaire(
    user: Annotated[AuthUser, Depends(current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    limit: int = Query(10, description="Количество записей, возвращаемых на одну страницу", ge=1, le=100),
    offset: int = Query(0, description="Смещение от начала списка записей", ge=0),
):
    return await crud.get_user_questionnaires(user, session, limit, offset)


@router.patch(
    "/{quest_id}",
    response_model=ResponseUserQuestionnaireSchema,
    status_code=status.HTTP_200_OK,
)
async def update_quest(
    quest_id: UUID,
    update_value: CreateUserQuestionnaireSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return await crud.update_questionnaire(quest_id, update_value, session)


@router.delete(
    "/{quest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_quest(
    user: Annotated[AuthUser, Depends(current_user)],
    quest_id: UUID,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return await crud.delete_quest(user, quest_id, session)
