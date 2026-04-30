from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.schemas.almacen import AlmacenCreate, AlmacenUpdate, AlmacenResponse
from app.services import almacen_service

router = APIRouter(prefix="/almacenes", tags=["almacenes"])

@router.get("", response_model=list[AlmacenResponse])
def get_almacenes(current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    return almacen_service.get_almacenes(tenant_schema)

@router.get("/{almacen_id}", response_model=AlmacenResponse)
def get_almacen(almacen_id: int, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    almacen = almacen_service.get_almacen_by_id(tenant_schema, almacen_id)
    if not almacen:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    return almacen

@router.post("", response_model=AlmacenResponse, status_code=status.HTTP_201_CREATED)
def create_almacen(data: AlmacenCreate, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    return almacen_service.create_almacen(tenant_schema, data)

@router.put("/{almacen_id}", response_model=AlmacenResponse)
def update_almacen(almacen_id: int, data: AlmacenUpdate, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    almacen = almacen_service.update_almacen(tenant_schema, almacen_id, data)
    if not almacen:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    return almacen

from sqlalchemy.exc import IntegrityError

@router.delete("/{almacen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_almacen(almacen_id: int, current_user: dict = Depends(get_current_user)):
    tenant_schema = current_user["tenant_schema"]
    try:
        success = almacen_service.delete_almacen(tenant_schema, almacen_id)
        if not success:
            raise HTTPException(status_code=404, detail="Almacén no encontrado")
    except IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar el almacén porque tiene registros de inventario u otros datos asociados."
        )
