from sqlalchemy import text

from app.core.security import verify_password
from app.db.session import engine


def get_tenant_by_schema(schema_name: str) -> dict | None:
    query = text(
        """
        SELECT tenant_id, schema_name, activo
        FROM shared.tenants
        WHERE schema_name = :schema_name
        """
    )
    with engine.connect() as connection:
        result = connection.execute(query, {"schema_name": schema_name}).mappings().first()
    return dict(result) if result else None


def get_user_for_tenant(tenant_id: int, username: str) -> dict | None:
    query = text(
        """
        SELECT usuario_id, username, password_hash, activo
        FROM shared.usuarios
        WHERE tenant_id = :tenant_id AND username = :username
        """
    )
    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"tenant_id": tenant_id, "username": username},
        ).mappings().first()
    return dict(result) if result else None


def get_user_roles(usuario_id: int) -> list[str]:
    query = text(
        """
        SELECT r.nombre
        FROM shared.usuario_rol ur
        INNER JOIN shared.roles r ON r.rol_id = ur.rol_id
        WHERE ur.usuario_id = :usuario_id
        ORDER BY r.nombre
        """
    )
    with engine.connect() as connection:
        rows = connection.execute(query, {"usuario_id": usuario_id}).mappings().all()
    return [row["nombre"] for row in rows]


def authenticate_user(username: str, password: str, tenant_schema: str) -> dict | None:
    tenant = get_tenant_by_schema(tenant_schema)
    if not tenant or not tenant["activo"]:
        return None

    user = get_user_for_tenant(tenant_id=tenant["tenant_id"], username=username)
    if not user or not user["activo"]:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    roles = get_user_roles(usuario_id=user["usuario_id"])
    return {
        "username": user["username"],
        "tenant_id": tenant["tenant_id"],
        "tenant_schema": tenant["schema_name"],
        "roles": roles,
    }
