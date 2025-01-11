from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import user, post, commnet
from auth import authentication


app = FastAPI()

# register router
app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(commnet.router)

# config static file
app.mount('/files', StaticFiles(directory='upload_files'), name='files')
