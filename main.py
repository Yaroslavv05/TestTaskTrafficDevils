import uvicorn

from fastapi import FastAPI
from core.database import init_db, init_db_roles_and_admin, AsyncSessionLocal
from api.v1.auth import router as auth_router_v1
from api.v1.requests import router as requests_router_v1
from api.v1.manage import router as manage_router_v1

app = FastAPI(
    title="Test Task Traffic Devils",
    version="1.0.0",
)

app.include_router(auth_router_v1)
app.include_router(manage_router_v1)
app.include_router(requests_router_v1)

@app.on_event("startup")
async def startup_event():
    await init_db()
    async with AsyncSessionLocal() as db:
        await init_db_roles_and_admin(db)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)