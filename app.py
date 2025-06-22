from fastapi import FastAPI
from user.interface.controller.user_controller import router as user_routers

app = FastAPI()

app.include_router(user_routers)