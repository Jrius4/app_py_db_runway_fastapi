from fastapi import FastAPI
import uvicorn
from server import models
from server.database import engine
from server.routers import blog,user,authentication

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=9000)


