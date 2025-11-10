from fastapi import APIRouter, Depends, status, Response

from app.services.search_service import SearchServices
from app.schemas.search_schema import SearchInput
from app.schemas.search_schema import SearchOutput

router = APIRouter(prefix="", tags=["Search"])


@router.get("/", response_model=SearchOutput, status_code=status.HTTP_200_OK)
def search_by_keyword(
    query_input: SearchInput = Depends(), service: SearchServices = Depends()
):
    result = service.search_by_keyword(query_input=query_input)
    return SearchOutput(
        courses=result.get("courses"),
        practice_tests=result.get("practice_tests")
    )
