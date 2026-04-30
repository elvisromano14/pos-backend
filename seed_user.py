import sys
import os

# Asegurar que podemos importar 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.db.session import engine
from app.core.security import get_password_hash

def seed_user():
    print("Conectando a la base de datos...")
    try:
        with engine.begin() as conn:
            # Check tenant
            tenant = conn.execute(text("SELECT tenant_id FROM shared.tenants WHERE schema_name = 'tenant_demo'")).scalar()
            if not tenant:
                print("Error: El tenant 'tenant_demo' no existe en la base de datos.")
                return

            # Hash the password
            hashed_pw = get_password_hash("admin123")

            # Check if user exists
            user_id = conn.execute(text("SELECT usuario_id FROM shared.usuarios WHERE username = 'admin' AND tenant_id = :t"), {"t": tenant}).scalar()
            
            if user_id:
                print("El usuario 'admin' ya existía. Actualizando su contraseña a 'admin123'...")
                conn.execute(
                    text("UPDATE shared.usuarios SET password_hash = :pw WHERE usuario_id = :uid"),
                    {"pw": hashed_pw, "uid": user_id}
                )
            else:
                print("Creando el usuario 'admin'...")
                result = conn.execute(
                    text("""
                        INSERT INTO shared.usuarios (tenant_id, username, email, password_hash, nombre, activo)
                        OUTPUT inserted.usuario_id
                        VALUES (:t, 'admin', 'admin@erp.com', :pw, 'Administrador', 1)
                    """),
                    {"t": tenant, "pw": hashed_pw}
                )
                user_id = result.scalar()

            # Asignar Rol
            role_id = conn.execute(text("SELECT rol_id FROM shared.roles WHERE nombre = 'Administrador' AND tenant_id = :t"), {"t": tenant}).scalar()
            if not role_id:
                result = conn.execute(
                    text("INSERT INTO shared.roles (tenant_id, nombre, descripcion) OUTPUT inserted.rol_id VALUES (:t, 'Administrador', 'Acceso Total')"),
                    {"t": tenant}
                )
                role_id = result.scalar()

            has_role = conn.execute(text("SELECT 1 FROM shared.usuario_rol WHERE usuario_id = :u AND rol_id = :r"), {"u": user_id, "r": role_id}).scalar()
            if not has_role:
                conn.execute(text("INSERT INTO shared.usuario_rol (usuario_id, rol_id) VALUES (:u, :r)"), {"u": user_id, "r": role_id})

            print("¡Éxito! El usuario 'admin' con clave 'admin123' está listo para hacer login.")
            
    except Exception as e:
        print(f"Ocurrió un error en la base de datos: {e}")

if __name__ == "__main__":
    seed_user()
