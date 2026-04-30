from sqlalchemy import text

from app.db.session import engine
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate

def get_categorias(tenant_schema: str) -> list[dict]:
    query = text(f"""
        SELECT categoria_id, nombre, descripcion, activo, fecha_creacion
        FROM [{tenant_schema}].categorias
    """)
    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()
    return [dict(row) for row in rows]

def get_categoria_by_id(tenant_schema: str, categoria_id: int) -> dict | None:
    query = text(f"""
        SELECT categoria_id, nombre, descripcion, activo, fecha_creacion
        FROM [{tenant_schema}].categorias
        WHERE categoria_id = :categoria_id
    """)
    with engine.connect() as connection:
        result = connection.execute(query, {"categoria_id": categoria_id}).mappings().first()
    return dict(result) if result else None

def create_categoria(tenant_schema: str, data: CategoriaCreate) -> dict:
    query = text(f"""
        INSERT INTO [{tenant_schema}].categorias (nombre, descripcion, activo)
        OUTPUT inserted.categoria_id, inserted.nombre, inserted.descripcion, inserted.activo, inserted.fecha_creacion
        VALUES (:nombre, :descripcion, :activo)
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {
            "nombre": data.nombre,
            "descripcion": data.descripcion,
            "activo": data.activo
        }).mappings().first()
    return dict(result)

def update_categoria(tenant_schema: str, categoria_id: int, data: CategoriaUpdate) -> dict | None:
    existing = get_categoria_by_id(tenant_schema, categoria_id)
    if not existing:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return existing

    set_clauses = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
    
    query = text(f"""
        UPDATE [{tenant_schema}].categorias
        SET {set_clauses}
        OUTPUT inserted.categoria_id, inserted.nombre, inserted.descripcion, inserted.activo, inserted.fecha_creacion
        WHERE categoria_id = :categoria_id
    """)
    
    params = {"categoria_id": categoria_id, **update_data}
    
    with engine.begin() as connection:
        result = connection.execute(query, params).mappings().first()
    return dict(result) if result else None

def delete_categoria(tenant_schema: str, categoria_id: int) -> bool:
    query = text(f"""
        DELETE FROM [{tenant_schema}].categorias
        WHERE categoria_id = :categoria_id
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {"categoria_id": categoria_id})
        return result.rowcount > 0
