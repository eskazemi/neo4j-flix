from src.core.container import Container
from src.services.auth import AuthService
from dependency_injector.wiring import (
    Provide,
    inject
)
from fastapi import (
    APIRouter,
    Depends,
)
from src.models.user import (
    User,
    UserSignIn,
    UserSignInResponse,
    UserSignUp,
    UserResetPassword
)

_tag_base = ["auth"]
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in", response_model=UserSignInResponse)
@inject
async def sign_in(user_info: UserSignIn, service: AuthService = Depends(
                    Provide[Container.auth_service])):
    return service.sign_in(user_info)


@router.post("/sign-up", response_model=User)
@inject
async def sign_up(new_user: UserSignUp,
                  service: AuthService = Depends(
                      Provide[Container.auth_service])):
    return service.sign_up(new_user)


@router.post("/reset-password", )
@inject
async def reset_password(user_reset_pass: UserResetPassword,
                         service: AuthService = Depends(
                             Provide[Container.auth_service])
                         ):
    """Reset User's password using user's email."""
    return service.reset_password(user_reset_pass)
