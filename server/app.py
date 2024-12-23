from fastapi import FastAPI
import uvicorn

from api.db.database import engine
from api.db.models import Base
from api.routes import api_version_one

app = FastAPI(
    title="Chat App",
    description="A simple chat application",
    version="0.1",
)

app.include_router(api_version_one)

@app.get("/")
def home():
    return {"Hello": "Docker!"}


Base.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)