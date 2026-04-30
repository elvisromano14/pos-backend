from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_current_user
from app.schemas.inventario import InventarioCreate, InventarioUpdate, InventarioResponse
from app.services import inventario_service

router = APIRouter(prefix="/inventarios", tags=["inventarios"])

@router.get("", response_model=list[InventarioResponse])
def get_inventarios(
    articulo_id: int | None = Query(None, description="Filtrar por ID de artículo"),
    almacen_id: int | None = Query(None, description="Filtrar por ID de almacén"),
    current_user: dict = Depends(get_current_user)
):
    tenant_schema = current_user["tenant_schema"]
    return inventario_service.get_inventarios(tenant_schema, articulo_id, almacen_id)

@router.get("/{inventario_id}", response_model=InventarioResponse)
def get_inventario(inventario_id: int, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    inventario = inventario_service.get_inventario_by_id(tenant_schema, inventario_id)
    if not inventario:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
    return inventario

@router.post("", response_model=InventarioResponse, status_code=status.HTTP_201_CREATED)
def create_inventario(data: InventarioCreate, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    
    try:
        return inventario_service.create_inventario(tenant_schema, data)
    except IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail="Error de integridad. Es posible que ya exista un registro para este artículo en este almacén, o el artículo/almacén no exista."
        )

@router.put("/{inventario_id}", response_model=InventarioResponse)
def update_inventario(inventario_id: int, data: InventarioUpdate, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    inventario = inventario_service.update_inventario(tenant_schema, inventario_id, data)
    if not inventario:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
    return inventario

@router.delete("/{inventario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventario(inventario_id: int, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    success = inventario_service.delete_inventario(tenant_schema, inventario_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado")
