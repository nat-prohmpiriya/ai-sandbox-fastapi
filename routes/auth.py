from fastapi import APIRouter
from typing import Dict 

router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/firebase/verify", response_model=Dict[str, str])
def firebase_verify():
    return {"message": "Firebase verification successful"}