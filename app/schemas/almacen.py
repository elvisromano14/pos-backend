from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AlmacenBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    direccion: str | None = None
    activo: bool = True

class AlmacenCreate(AlmacenBase):
    pass

class AlmacenUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    direccion: str | None = None
    activo: bool | None = None

class AlmacenResponse(AlmacenBase):
    almacen_id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)
