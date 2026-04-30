from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.services import categoria_service

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("", response_model=list[CategoriaResponse])
def get_categorias(current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    return categoria_service.get_categorias(tenant_schema)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def get_categoria(categoria_id: int, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    categoria = categoria_service.get_categoria_by_id(tenant_schema, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def create_categoria(data: CategoriaCreate, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    return categoria_service.create_categoria(tenant_schema, data)

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def update_categoria(categoria_id: int, data: CategoriaUpdate, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    categoria = categoria_service.update_categoria(tenant_schema, categoria_id, data)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

from sqlalchemy.exc import IntegrityError

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(categoria_id: int, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    try:
        success = categoria_service.delete_categoria(tenant_schema, categoria_id)
        if not success:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    except IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar la categoría porque está siendo utilizada por uno o más artículos."
        )
