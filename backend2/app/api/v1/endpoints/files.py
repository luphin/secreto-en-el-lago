"""
Endpoints para gestión de archivos (fotos y huellas digitales)
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.core.storage import storage_manager
from app.core.database import get_database
from app.services.user_service import UserService
from app.api.dependencies import get_current_user
from app.models.user import UserResponse, UserUpdate

router = APIRouter()


@router.post("/upload/photo", response_model=dict)
async def upload_photo(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Sube una foto de usuario a MinIO
    """
    # Validar tipo de archivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser una imagen"
        )
    
    # Validar tamaño (máximo 5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La imagen no puede superar los 5MB"
        )
    
    # Subir a MinIO
    import io
    file_data = io.BytesIO(contents)
    url = await storage_manager.upload_photo(file_data, str(current_user["_id"]))
    
    if not url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al subir la foto"
        )
    
    # Actualizar usuario con la URL de la foto
    user_service = UserService(db)
    await user_service.update_user(
        str(current_user["_id"]),
        UserUpdate(foto_url=url)
    )
    
    return {
        "message": "Foto subida exitosamente",
        "url": url
    }


@router.post("/upload/fingerprint", response_model=dict)
async def upload_fingerprint(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Sube datos de huella digital a MinIO
    """
    # Validar tamaño (máximo 1MB)
    contents = await file.read()
    if len(contents) > 1 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo de huella no puede superar 1MB"
        )
    
    # Subir a MinIO
    import io
    file_data = io.BytesIO(contents)
    url = await storage_manager.upload_fingerprint(file_data, str(current_user["_id"]))
    
    if not url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al subir la huella digital"
        )
    
    # Actualizar usuario con la referencia de la huella
    user_service = UserService(db)
    await user_service.update_user(
        str(current_user["_id"]),
        UserUpdate(huella_ref=url)
    )
    
    return {
        "message": "Huella digital subida exitosamente",
        "reference": url
    }


@router.delete("/delete/photo", response_model=dict)
async def delete_photo(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Elimina la foto de usuario
    """
    if not current_user.get("foto_url"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay foto para eliminar"
        )
    
    # Extraer nombre del objeto de la URL
    object_name = f"photos/{current_user['_id']}.jpg"
    
    # Eliminar de MinIO
    await storage_manager.delete_file(object_name)
    
    # Actualizar usuario
    user_service = UserService(db)
    await user_service.update_user(
        str(current_user["_id"]),
        UserUpdate(foto_url=None)
    )
    
    return {"message": "Foto eliminada exitosamente"}

