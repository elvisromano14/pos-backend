from datetime import datetime
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class ArticuloBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: str | None = None
    categoria_id: int
    unidad_medida: str = "UND"
    costo_promedio: Decimal = Decimal("0.0000")
    precio_base: Decimal = Decimal("0.0000")
    aplica_iva: bool = True
    aplica_igtf: bool = False
    activo: bool = True

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloUpdate(BaseModel):
    codigo: str | None = None
    nombre: str | None = None
    descripcion: str | None = None
    categoria_id: int | None = None
    unidad_medida: str | None = None
    costo_promedio: Decimal | None = None
    precio_base: Decimal | None = None
    aplica_iva: bool | None = None
    aplica_igtf: bool | None = None
    activo: bool | None = None

class ArticuloResponse(ArticuloBase):
    articulo_id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)
