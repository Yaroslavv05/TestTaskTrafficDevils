import uvicorn

from fastapi import FastAPI
from api.v1.auth import router as auth_router_v1
from api.v1.requests import router as requests_router_v1
from core.database import init_db, init_db_roles
import asyncio

asyncio.run(init_db)
asyncio.run(init_db_roles)

app = FastAPI(
    title="Test Task Traffic Devils",
    version="1.1.0",
)

app.include_router(auth_router_v1)
app.include_router(requests_router_v1)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
