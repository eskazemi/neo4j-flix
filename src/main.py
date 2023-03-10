from src.api.routes import api_router
from src.app import app


@app.on_event("startup")
async def on_app_start():
    """Anything that needs to be done while app starts
    """
    pass


@app.on_event("shutdown")
async def on_app_shutdown():
    from src.config import get_setting
    get_setting.cache_clear()
    """Anything that needs to be done while app shutdown
    """
    pass


# ###########End connect###############

app.include_router(api_router)
