from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_current_user
from app.schemas.articulo import ArticuloCreate, ArticuloUpdate, ArticuloResponse
from app.services import articulo_service

router = APIRouter(prefix="/articulos", tags=["articulos"])

@router.get("", response_model=list[ArticuloResponse])
def get_articulos(current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    return articulo_service.get_articulos(tenant_schema)

@router.get("/{articulo_id}", response_model=ArticuloResponse)
def get_articulo(articulo_id: int, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    articulo = articulo_service.get_articulo_by_id(tenant_schema, articulo_id)
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return articulo

@router.post("", response_model=ArticuloResponse, status_code=status.HTTP_201_CREATED)
def create_articulo(data: ArticuloCreate, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    try:
        return articulo_service.create_articulo(tenant_schema, data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error de integridad. Verifique que el código no exista o que la categoría sea válida.")

@router.put("/{articulo_id}", response_model=ArticuloResponse)
def update_articulo(articulo_id: int, data: ArticuloUpdate, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    try:
        articulo = articulo_service.update_articulo(tenant_schema, articulo_id, data)
        if not articulo:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")
        return articulo
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar.")

@router.delete("/{articulo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_articulo(articulo_id: int, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    try:
        success = articulo_service.delete_articulo(tenant_schema, articulo_id)
        if not success:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")
    except IntegrityError:
        raise HTTPException(status_code=400, detail="No se puede eliminar el artículo. Es probable que esté en uso en inventario o ventas.")
