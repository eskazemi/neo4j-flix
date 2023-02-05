from fastapi import (
    APIRouter,
    Depends
)
from src.core.container import Container
from dependency_injector.wiring import (
    Provide,
    inject
)
from src.services.user import UserService
from src.models.user import (
    UserChangePassword,
    UserUpdate
)

_tag_base = ["User"]

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/change-password", tags=_tag_base)
@inject
async def change_password(
        user_change_pass: UserChangePassword,
        service: UserService = Depends(Provide[Container.auth_service])
):
    """Change User's password."""
    pass


@router.get("/{user_id}", tags=_tag_base)
@inject
async def get_profile(
        user_id: str,
        service: UserService = Depends(Provide[Container.auth_service])):
    pass


@router.patch("/{user_id}", tags=_tag_base)
@inject
async def update_profile(user_id: str, attributes: UserUpdate,
                         service: UserService = Depends(
                             Provide[Container.auth_service]
                         )):
    """Add check to stop call if password is being changed."""
    pass
