from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    # TODO: Reemplazar por validacion contra SQL Server shared.usuarios
    if payload.username != "admin" or payload.password != "admin123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    token = create_access_token(
        subject=payload.username,
        tenant_schema=payload.tenant_schema,
    )
    return TokenResponse(access_token=token)
