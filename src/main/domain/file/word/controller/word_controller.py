from fastapi import APIRouter

router = APIRouter(prefix="/file/word", tags=["Word"])

@router.post("/")
def create_word_file():
    pass