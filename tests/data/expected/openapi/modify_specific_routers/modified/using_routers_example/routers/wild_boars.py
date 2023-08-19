# generated by fastapi-codegen:
#   filename:  using_routers_example.yaml
#   timestamp: 2023-04-11T00:00:00+00:00

from __future__ import annotations

from fastapi import APIRouter

from ..dependencies import *

router = APIRouter(tags=['Wild Boars'])


@router.get('/boars', response_model=WildBoars, tags=['Wild Boars'])
def list_wild_boars(limit: Optional[int] = None) -> WildBoars:
    """
    List All Wild Boars
    """
    pass


@router.post('/boars', response_model=None, tags=['Wild Boars'])
def create_wild_boars() -> None:
    """
    Create a Wild Boar
    """
    pass


@router.get('/boars/{boar_id}', response_model=Pet, tags=['Wild Boars'])
def show_boar_by_id(boar_id: str = Path(..., alias='boarId')) -> Pet:
    """
    Info For a Specific Boar
    """
    pass