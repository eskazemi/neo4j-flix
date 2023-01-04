from urls import api_router
from fastapi.middleware.cors import CORSMiddleware
from src.app import app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ###########EndCROS###############

@app.on_event("startup")
async def on_app_start():
    """Anything that needs to be done while app starts
    """
    pass


@app.on_event("shutdown")
async def on_app_shutdown():
    """Anything that needs to be done while app shutdown
    """
    pass


# ###########End connect###############

app.include_router(api_router)
