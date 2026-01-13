from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pathlib import Path
from . import static
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import uvicorn
from .routers import user
from .models.custom import make_custom_response
from .auth import init_auth

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, e: HTTPException):
    return JSONResponse(
        content=make_custom_response(code=0, msg=str(e), data=None).model_dump(),
        status_code=200,
    )


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(
    request: Request, e: RequestValidationError
):
    return JSONResponse(
        content=make_custom_response(code=0, msg=str(e), data=None).model_dump(),
        status_code=200,
    )


init_auth(app)

app.mount("/static", StaticFiles(directory=Path(static.__file__).parent), name="static")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="static/favicon.png",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_oauth2_redirect_html():
    return get_swagger_ui_oauth2_redirect_html()


def main():
    uvicorn.run(app=app, host="0.0.0.0")


if __name__ == "__main__":
    main()
