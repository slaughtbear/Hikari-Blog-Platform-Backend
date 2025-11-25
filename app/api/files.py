from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from app.authentication.tokens import get_current_user
from app.models.users import User
from app.services.services import process_file


router = APIRouter()


@router.post("/upload/", status_code = status.HTTP_204_NO_CONTENT)
async def upload_file(
    file: UploadFile,
    current_user: User = Depends(get_current_user)
):
    response = await process_file(file)
    
    if not response:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No fue posible subir el archivo..."
        )