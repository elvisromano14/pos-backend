from sqlalchemy import text

from app.db.session import engine
from app.schemas.almacen import AlmacenCreate, AlmacenUpdate

def get_almacenes(tenant_schema: str) -> list[dict]:
    query = text(f"""
        SELECT almacen_id, nombre, descripcion, direccion, activo, fecha_creacion
        FROM [{tenant_schema}].almacenes
    """)
    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()
    return [dict(row) for row in rows]

def get_almacen_by_id(tenant_schema: str, almacen_id: int) -> dict | None:
    query = text(f"""
        SELECT almacen_id, nombre, descripcion, direccion, activo, fecha_creacion
        FROM [{tenant_schema}].almacenes
        WHERE almacen_id = :almacen_id
    """)
    with engine.connect() as connection:
        result = connection.execute(query, {"almacen_id": almacen_id}).mappings().first()
    return dict(result) if result else None

def create_almacen(tenant_schema: str, data: AlmacenCreate) -> dict:
    query = text(f"""
        INSERT INTO [{tenant_schema}].almacenes (nombre, descripcion, direccion, activo)
        OUTPUT inserted.almacen_id, inserted.nombre, inserted.descripcion, inserted.direccion, inserted.activo, inserted.fecha_creacion
        VALUES (:nombre, :descripcion, :direccion, :activo)
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {
            "nombre": data.nombre,
            "descripcion": data.descripcion,
            "direccion": data.direccion,
            "activo": data.activo
        }).mappings().first()
    return dict(result)

def update_almacen(tenant_schema: str, almacen_id: int, data: AlmacenUpdate) -> dict | None:
    # First, get the existing record to merge fields
    existing = get_almacen_by_id(tenant_schema, almacen_id)
    if not existing:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return existing

    set_clauses = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
    
    query = text(f"""
        UPDATE [{tenant_schema}].almacenes
        SET {set_clauses}
        OUTPUT inserted.almacen_id, inserted.nombre, inserted.descripcion, inserted.direccion, inserted.activo, inserted.fecha_creacion
        WHERE almacen_id = :almacen_id
    """)
    
    params = {"almacen_id": almacen_id, **update_data}
    
    with engine.begin() as connection:
        result = connection.execute(query, params).mappings().first()
    return dict(result) if result else None

def delete_almacen(tenant_schema: str, almacen_id: int) -> bool:
    query = text(f"""
        DELETE FROM [{tenant_schema}].almacenes
        WHERE almacen_id = :almacen_id
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {"almacen_id": almacen_id})
        return result.rowcount > 0
