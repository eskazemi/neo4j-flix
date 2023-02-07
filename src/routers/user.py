from fastapi import (
    APIRouter,
    Depends
)
from src.core.dependencies import get_current_active_user
from src.core.container import Container
from dependency_injector.wiring import (
    Provide,
    inject
)
from src.models.user import (
    User,
    UserUpdate,
)
from src.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=User)
@inject
async def my_profile(current_user: User = Depends(get_current_active_user)):
    """GET Current user's information."""
    return current_user


@router.get("/{user_id}")
@inject
async def get_profile(user_id: str, service: UserService = Depends(
    Provide[Container.user_service])):
    return service.get_profile(user_id)


@router.patch("/{user_id}")
@inject
async def update_profile(user_id: str,
                         attributes: UserUpdate,
                         service: UserService =Depends(Provide[Container.user_service])):
    """Add check to stop call if password is being changed."""
    attributes = dict(attributes)
    return service.update_profile(attributes, user_id)


