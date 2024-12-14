from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def ping():
    """
    Health check
    """
    return "OK"
