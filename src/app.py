from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------app -----------------------------------


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
]

app = FastAPI(
    title="recommendations sandbox",
    version="1.0.0",
    docs_url='/api/docs',
    redoc_url='/api/redoc',
    openapi_url='/api/openapi.json',
    middleware=middleware,
    debug=True
)



def custom_openapi():
    # cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # custom settings
    openapi_schema = get_openapi(
        title="recommendations sandbox",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    # setting new logo to docs
    openapi_schema["info"]["x-logo"] = {
        "url": "https://assets.nflxext.com/ffe/siteui/vlv3/"
               "84526d58-475e-4e6f-9c81-d2d78ddce803/"
               "62d12460-97e8-4be6-8ba6-d8adddfabdf2/"
               "GB-en-20221228-popsignuptwoweeks-perspective_alpha_website_large.jpg"
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# assign the customized OpenAPI schema
app.openapi = custom_openapi
