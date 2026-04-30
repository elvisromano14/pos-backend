import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.db.session import engine

def create_tables():
    tenant_schema = "tenant_demo"
    print(f"Creating tables for {tenant_schema}...")
    
    with engine.begin() as conn:
        try:
            conn.execute(text(f"""
            CREATE TABLE [{tenant_schema}].almacenes (
                almacen_id INT IDENTITY(1,1) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion VARCHAR(255),
                direccion VARCHAR(255),
                activo BIT NOT NULL DEFAULT 1,
                fecha_creacion DATETIME NOT NULL DEFAULT GETDATE()
            );
            """))
            print("Table almacenes created.")
        except Exception as e:
            print("Table almacenes might already exist:", e)

        try:
            conn.execute(text(f"""
            CREATE TABLE [{tenant_schema}].categorias (
                categoria_id INT IDENTITY(1,1) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion VARCHAR(255),
                activo BIT NOT NULL DEFAULT 1,
                fecha_creacion DATETIME NOT NULL DEFAULT GETDATE()
            );
            """))
            print("Table categorias created.")
        except Exception as e:
            print("Table categorias might already exist:", e)

        try:
            conn.execute(text(f"""
            CREATE TABLE [{tenant_schema}].articulos (
                articulo_id INT IDENTITY(1,1) PRIMARY KEY,
                codigo VARCHAR(50) NOT NULL UNIQUE,
                nombre VARCHAR(150) NOT NULL,
                descripcion VARCHAR(500),
                categoria_id INT NOT NULL FOREIGN KEY REFERENCES [{tenant_schema}].categorias(categoria_id),
                unidad_medida VARCHAR(20) NOT NULL DEFAULT 'UNIDAD',
                costo_promedio DECIMAL(18,4) NOT NULL DEFAULT 0,
                precio_base DECIMAL(18,4) NOT NULL DEFAULT 0,
                aplica_iva BIT NOT NULL DEFAULT 1,
                aplica_igtf BIT NOT NULL DEFAULT 0,
                activo BIT NOT NULL DEFAULT 1,
                fecha_creacion DATETIME NOT NULL DEFAULT GETDATE()
            );
            """))
            print("Table articulos created.")
        except Exception as e:
            print("Table articulos might already exist:", e)

if __name__ == "__main__":
    create_tables()
