from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import user
from router import post

app = FastAPI()

# register router
app.include_router(user.router)
app.include_router(post.router)

# config static file
app.mount('/files', StaticFiles(directory='upload_files'), name='files')
