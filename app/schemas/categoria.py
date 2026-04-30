from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    activo: bool = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    activo: bool | None = None

class CategoriaResponse(CategoriaBase):
    categoria_id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)
