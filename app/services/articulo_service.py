from sqlalchemy import text

from app.db.session import engine
from app.schemas.articulo import ArticuloCreate, ArticuloUpdate

def get_articulos(tenant_schema: str) -> list[dict]:
    query = text(f"""
        SELECT articulo_id, codigo, nombre, descripcion, categoria_id,
               unidad_medida, costo_promedio, precio_base, aplica_iva,
               aplica_igtf, activo, fecha_creacion
        FROM [{tenant_schema}].articulos
    """)
    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()
    return [dict(row) for row in rows]

def get_articulo_by_id(tenant_schema: str, articulo_id: int) -> dict | None:
    query = text(f"""
        SELECT articulo_id, codigo, nombre, descripcion, categoria_id,
               unidad_medida, costo_promedio, precio_base, aplica_iva,
               aplica_igtf, activo, fecha_creacion
        FROM [{tenant_schema}].articulos
        WHERE articulo_id = :articulo_id
    """)
    with engine.connect() as connection:
        result = connection.execute(query, {"articulo_id": articulo_id}).mappings().first()
    return dict(result) if result else None

def create_articulo(tenant_schema: str, data: ArticuloCreate) -> dict:
    query = text(f"""
        INSERT INTO [{tenant_schema}].articulos 
        (codigo, nombre, descripcion, categoria_id, unidad_medida, 
         costo_promedio, precio_base, aplica_iva, aplica_igtf, activo)
        OUTPUT inserted.articulo_id, inserted.codigo, inserted.nombre, inserted.descripcion, 
               inserted.categoria_id, inserted.unidad_medida, inserted.costo_promedio, 
               inserted.precio_base, inserted.aplica_iva, inserted.aplica_igtf, 
               inserted.activo, inserted.fecha_creacion
        VALUES 
        (:codigo, :nombre, :descripcion, :categoria_id, :unidad_medida, 
         :costo_promedio, :precio_base, :aplica_iva, :aplica_igtf, :activo)
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {
            "codigo": data.codigo,
            "nombre": data.nombre,
            "descripcion": data.descripcion,
            "categoria_id": data.categoria_id,
            "unidad_medida": data.unidad_medida,
            "costo_promedio": data.costo_promedio,
            "precio_base": data.precio_base,
            "aplica_iva": data.aplica_iva,
            "aplica_igtf": data.aplica_igtf,
            "activo": data.activo
        }).mappings().first()
    return dict(result)

def update_articulo(tenant_schema: str, articulo_id: int, data: ArticuloUpdate) -> dict | None:
    existing = get_articulo_by_id(tenant_schema, articulo_id)
    if not existing:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return existing

    set_clauses = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
    
    query = text(f"""
        UPDATE [{tenant_schema}].articulos
        SET {set_clauses}
        OUTPUT inserted.articulo_id, inserted.codigo, inserted.nombre, inserted.descripcion, 
               inserted.categoria_id, inserted.unidad_medida, inserted.costo_promedio, 
               inserted.precio_base, inserted.aplica_iva, inserted.aplica_igtf, 
               inserted.activo, inserted.fecha_creacion
        WHERE articulo_id = :articulo_id
    """)
    
    params = {"articulo_id": articulo_id, **update_data}
    
    with engine.begin() as connection:
        result = connection.execute(query, params).mappings().first()
    return dict(result) if result else None

def delete_articulo(tenant_schema: str, articulo_id: int) -> bool:
    query = text(f"""
        DELETE FROM [{tenant_schema}].articulos
        WHERE articulo_id = :articulo_id
    """)
    with engine.begin() as connection:
        result = connection.execute(query, {"articulo_id": articulo_id})
        return result.rowcount > 0
