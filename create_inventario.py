import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.db.session import engine

def create_tables():
    tenant_schema = "tenant_demo"
    
    with engine.begin() as conn:
        try:
            conn.execute(text(f"""
            CREATE TABLE [{tenant_schema}].inventario (
                inventario_id INT IDENTITY(1,1) PRIMARY KEY,
                articulo_id INT NOT NULL FOREIGN KEY REFERENCES [{tenant_schema}].articulos(articulo_id),
                almacen_id INT NOT NULL FOREIGN KEY REFERENCES [{tenant_schema}].almacenes(almacen_id),
                existencia DECIMAL(18,4) NOT NULL DEFAULT 0,
                ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
                CONSTRAINT UQ_inv_art_alm_{tenant_schema} UNIQUE(articulo_id, almacen_id)
            );
            """))
            print("Table inventario created.")
        except Exception as e:
            print("Table inventario might already exist:", e)

if __name__ == "__main__":
    create_tables()
