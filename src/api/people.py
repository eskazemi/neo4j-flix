from fastapi import (
    APIRouter,
    Depends
)
from src.core.container import Container
from dependency_injector.wiring import (
    Provide,
    inject
)
from src.services.people import PeopleService


people_routes = APIRouter(prefix="/people", tags=["People"])


@people_routes.get('/')
@inject
def get_index(service: PeopleService = Depends(
                    Provide[Container.people_service])):
    # Get Pagination Values
    # q = request.args.get("q")
    # sort = request.args.get("sort", "title")
    # order = request.args.get("order", "ASC")
    # limit = request.args.get("limit", 6, type=int)
    # skip = request.args.get("skip", 0, type=int)
    pass


@people_routes.get('/{id}')
@inject
def get_person(id, service: PeopleService = Depends(
                    Provide[Container.people_service])):
    # Create an instance of the PeopleDAO
    pass


@people_routes.get('/{id}/similar')
@inject
def get_similar_people(id, service: PeopleService = Depends(
                    Provide[Container.people_service])):
    # Get Pagination Values
    # limit = request.args.get("limit", 6, type=int)
    # skip = request.args.get("skip", 0, type=int)
    pass
