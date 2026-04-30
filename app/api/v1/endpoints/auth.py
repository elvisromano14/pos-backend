from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.schemas.auth import CurrentUserResponse, LoginRequest, TokenResponse
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    auth_result = authenticate_user(
        username=payload.username,
        password=payload.password,
        tenant_schema=payload.tenant_schema,
    )
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    token = create_access_token(
        subject=auth_result["username"],
        tenant_id=auth_result["tenant_id"],
        tenant_schema=auth_result["tenant_schema"],
        roles=auth_result["roles"],
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=CurrentUserResponse)
def me(current_user: dict = Depends(get_current_user)) -> CurrentUserResponse:
    return CurrentUserResponse(
        username=current_user["sub"],
        tenant_id=int(current_user["tenant_id"]),
        tenant_schema=current_user["tenant_schema"],
        roles=list(current_user["roles"]),
    )
