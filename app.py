from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from common.middlewares import create_middlewares
from user.interface.controller.user_controller import router as user_routers
from note.interface.controller.note_controller import router as note_routers
from containers import Container

app = FastAPI()
container = Container()
app.container = container

create_middlewares(app)

container.wire(
    modules=[
        "user.interface.controller.user_controller",
        "note.interface.controller.note_controller",
    ]
)

app.include_router(user_routers)
app.include_router(note_routers)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )
