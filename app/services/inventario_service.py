from sqlalchemy import text

from app.db.session import engine
from app.schemas.inventario import InventarioCreate, InventarioUpdate

def get_inventarios(tenant_schema: str, articulo_id: int | None = None, almacen_id: int | None = None) -> list[dict]:
    # Allows filtering by articulo_id or almacen_id
    base_query = f"""
        SELECT inventario_id, articulo_id, almacen_id, existencia, ultima_actualizacion
        FROM [{tenant_schema}].inventario
        WHERE 1=1
    """
    params = {}
    if articulo_id is not None:
        base_query += " AND articulo_id = :articulo_id"
        params["articulo_id"] = articulo_id
    if almacen_id is not None:
        base_query += " AND almacen_id = :almacen_id"
        params["almacen_id"] = almacen_id
        
    with engine.connect() as connection:
        rows = connection.execute(text(base_query), params).mappings().all()
    return [dict(row) for row in rows]

def get_inventario_by_id(tenant_schema: str, inventario_id: int) -> dict | None:
    query = text(f"""
        SELECT inventario_id, articulo_id, almacen_id, existencia, ultima_actualizacion
        FROM [{tenant_schema}].inventario
        WHERE inventario_id = :inventario_id
    """)
    with engine.connect() as connection:
        result = connection.execute(query, {"inventario_id": inventario_id}).mappings().first()
    return dict(result) if result else None

def get_inventario_by_articulo_and_almacen(tenant_schema: str, articulo_id: int, almacen_id: int) -> dict | None:
    query = text(f"""
        SELECT inventario_id, articulo_id, almacen_id, existencia, ultima_actualizacion
        FROM [{tenant_schema}].inventario
        WHERE articulo_id = :articulo_id AND almacen_id = :almacen_id
    """)
    with engine.connect() as connection:
        result = connection.execute(query, {
            "articulo_id": articulo_id, 
            "almacen_id": almacen_id
        }).mappings().first()
    return dict(result) if result else None

def create_inventario(tenant_schema: str, data: InventarioCreate) -> dict:
    query = text(f"""
        INSERT INTO [{tenant_schema}].inventario (articulo_id, almacen_id, existencia)
        OUTPUT inserted.inventario_id, inserted.articulo_id, inserted.almacen_id, inserted.existencia, inserted.ultima_actualizacion
        VALUES (:articulo_id, :almacen_id, :existencia)
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {
            "articulo_id": data.articulo_id,
            "almacen_id": data.almacen_id,
            "existencia": data.existencia
        }).mappings().first()
    return dict(result)

def update_inventario(tenant_schema: str, inventario_id: int, data: InventarioUpdate) -> dict | None:
    query = text(f"""
        UPDATE [{tenant_schema}].inventario
        SET existencia = :existencia
        OUTPUT inserted.inventario_id, inserted.articulo_id, inserted.almacen_id, inserted.existencia, inserted.ultima_actualizacion
        WHERE inventario_id = :inventario_id
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {
            "inventario_id": inventario_id,
            "existencia": data.existencia
        }).mappings().first()
    return dict(result) if result else None

def update_existencia(tenant_schema: str, articulo_id: int, almacen_id: int, cantidad_ajuste: float) -> dict | None:
    # Utility method to easily add/subtract inventory directly without fetching first
    query = text(f"""
        UPDATE [{tenant_schema}].inventario
        SET existencia = existencia + :cantidad_ajuste
        OUTPUT inserted.inventario_id, inserted.articulo_id, inserted.almacen_id, inserted.existencia, inserted.ultima_actualizacion
        WHERE articulo_id = :articulo_id AND almacen_id = :almacen_id
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {
            "articulo_id": articulo_id,
            "almacen_id": almacen_id,
            "cantidad_ajuste": cantidad_ajuste
        }).mappings().first()
    return dict(result) if result else None

def delete_inventario(tenant_schema: str, inventario_id: int) -> bool:
    query = text(f"""
        DELETE FROM [{tenant_schema}].inventario
        WHERE inventario_id = :inventario_id
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {"inventario_id": inventario_id})
        return result.rowcount > 0
