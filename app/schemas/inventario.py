from datetime import datetime
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class InventarioBase(BaseModel):
    articulo_id: int
    almacen_id: int
    existencia: Decimal = Decimal("0.0000")

class InventarioCreate(InventarioBase):
    pass

class InventarioUpdate(BaseModel):
    existencia: Decimal

class InventarioResponse(InventarioBase):
    inventario_id: int
    ultima_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
