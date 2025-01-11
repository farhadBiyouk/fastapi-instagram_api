from fastapi import FastAPI
from router import user

app = FastAPI()

# register router
app.include_router(user.router)
